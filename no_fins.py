import numpy as np
import copy
from numba import jit
import time

np.set_printoptions(precision = 5,suppress = True)

iterations = 200
multiple = 2
Ta = 20



kappa_micro = 150
kappa_ceramic = 230
kappa_heat_sink = 248
dist = (1/multiple)*10**(-3)
p = 0.5*10**9

height_a =copy.copy(multiple)
width_a = multiple*14
height_b = multiple*2
width_b = multiple*20
height_c = multiple*4
width_c = 50
print(height_a,width_a)
print(height_b,width_b)
print(height_c,width_c)


@jit(nopython = True,parallel = True)
def solver(input_array,tot_power):

    m = input_array.shape[0]
    n = input_array.shape[1]
    for i in range(1,m-1):
        for j in range(1,n-1):
            input_array[i][j] = 0.25*(input_array[i-1][j]+input_array[i+1][j]+input_array[i][j+1]+input_array[i][j-1]+dist**2*tot_power*(1/kappa_micro))
            #input_array[i][j] = 0.25*(input_array[i-1][j]+input_array[i+1][j]+input_array[i][j+1]+input_array[i][j-1])
    #input_array[2:m-2,2:n-2] = 0.25*(np.roll(input_array,1)+np.roll(input_array,-1)+
    #                     np.roll(input_array,1,axis = 0)+np.roll(input_array,-1,axis = 0)+dist**2*p*(1/kappa)*np.ones((m,n)))[2:m-2,2:n-2]        
    return input_array
    


@jit(nopython = True,parallel = True)
def derivatives_maker(input_array,left,right,kappa):
    m = input_array.shape[0]
    n = input_array.shape[1]
    #input_array[2:m-2,0] = 1.31 * (input_array[2:m-2,2]-Ta)**(4/3)/kappa
    input_array[1:m-1,0] = input_array[1:m-1,2] - 2*dist* 1.31 * (input_array[1:m-1,1]-Ta)**(4/3)/kappa    

    #input_array[2:m-2,n-1] = 1.31 *(input_array[2:m-2,n-3]-Ta)**(4/3)/kappa

    #input_array[2:m-2,n-2] = input_array[2:m-2,n-4] - 2*dist*input_array[2:m-2,n-1]

    input_array[1:m-1,n-1] = input_array[1:m-1,n-3] - 2*dist* 1.31 * (input_array[1:m-1,n-2]-Ta)**(4/3)/kappa    
    #input_array[0,2:n-2] = 1.31*(input_array[2,2:n-2]-Ta)**(4/3)/kappa



    #input_array[m-1,2:2+left] = 1.31*(input_array[m-3,2:2+left]-Ta)**(4/3)/kappa

    input_array[m-1,1:int(left+1)] = input_array[m-3,1:int(left+1)] - 2*dist* 1.31 * (input_array[m-2,1:int(left+1)]-Ta)**(4/3)/kappa    



    input_array[m-1,int(n-1-right):n-1] = input_array[m-3,int(n-1-right):n-1] - 2*dist* 1.31 * (input_array[m-2,int(n-1-right):n-1]-Ta)**(4/3)/kappa    



    #for i in range(2,m-2):
        #h = 1.31 *np.cbrt(np.abs((input_array[i][2]-Ta)))
        #input_array[i][0] = h*(input_array[i][2]-Ta)/kappa
        
        #h = 1.31 *np.cbrt(np.abs((input_array[i][n-3]-Ta)))
        #input_array[i][n-1] = h*(input_array[i][n-3]-Ta)/kappa

#    for j in range(2,n-2):
#        h = 1.31 *np.cbrt(np.abs((input_array[2][j]-Ta)))
#        input_array[0][j] = h*(input_array[2][j]-Ta)/kappa
#        
#        h = 1.31 *np.cbrt(np.abs((input_array[m-3][j]-Ta)))
#        input_array[m-1][j] = h*(input_array[m-3][j]-Ta)/kappa
    return input_array


#def imag_point_maker(input_array):
#    m = np.shape(input_array)[0]
#    n = np.shape(input_array)[1]
#    input_array[2:m-2,1] = input_array[2:m-2,3] - 2*dist*input_array[2:m-2,0]
#    input_array[2:m-2,n-2] = input_array[2:m-2,n-4] - 2*dist*input_array[2:m-2,n-1]
#    input_array[1,2:n-2] = input_array[3,2:n-2] - 2*dist*input_array[0,2:n-2]
#    input_array[m-2,2:n-2] = input_array[m-4,2:n-2] - 2*dist*input_array[m-1,2:n-2]   
#    return input_array
    

def run_block_a(a):
    #print(a)
    a = derivatives_maker(a,(a.shape[1])/2+1,(a.shape[1])/2+1,kappa_micro)
    #print(a)
    a = solver(a,p)
    return a
def run_block_b(b):
    b = derivatives_maker(b,(width_b-width_a)/2,(width_b-width_a)/2,kappa_ceramic)
    b = solver(b,0)
    #print(b.shape)
    return b
def run_block_c(c):
    c = derivatives_maker(c,(width_c-width_b)/2,(width_c-width_b)/2,kappa_heat_sink)
    #need to add top derivatives
    c[0,1:width_c-1] =c[2,1:width_c-1] - 2*dist*1.31 * (c[1,1:width_c-1] - Ta)**(4/3)/kappa_heat_sink
    c = solver(c,0)
    #print(c.shape)
    return c




def my_running(input_array):
    
    m = np.shape(input_array)[0]
    n = np.shape(input_array)[1]
    for i in range(iterations):
        run_block_a(input_array[m-height_a-2:m,int((n-width_a)/2):int((n+width_a)/2)])#include 1 row of b
        #run_block_a(input_array[int((n-width_a)/2):int((n+width_a)/2),m-height_a-2:m])#include 1 row of b
        run_block_b(input_array[m-height_a - height_b-2:m-height_a,int((n-width_b)/2):int((n+width_b)/2)]) 
        run_block_c(input_array[0:height_c+2,int((n-width_c)/2):int((n+width_c)/2)]) #include 1 row of b

    return input_array

test = np.ones((height_a+height_b+height_c+2,width_c))*20
bob = my_running(test)
#b = np.ones((length+4,width+4))*40
#print("b")
#print(b)
#c = derivatives_maker(b,2,4)
#np.savetxt('c.txt',c,delimiter = ',')
#print("c")
#print(c)
#d = solver(c)
#print("d")
#print(d)

np.savetxt('out.txt',bob,delimiter = ',')




#a[3,3] = 30
#a[3,4] = 40
#plengthlengtrint("a")
#print(a)
#b = solver(a)
#print("b")
#print(b)

#c = derivatives_maker(b)
#print("c")
#print(c)
#d = imag_point_maker(c)
#print("d")
#print(d)

#for i in range(2*10**5):
    #b = derivatives_maker(b)
    #b = imag_point_maker(b)
    #b = solver(b)
    
    
#start = time.time()
#before = 1
#after = 1
#error = 100
#while np.abs(error) > 1e-14:
    #m = np.shape(b)[0]
    #n = np.shape(b)[1]
    #before = copy.copy(after)
    #b = derivatives_maker(b)
    #b = imag_point_maker(b)
    #b = solver(b)
    #after = np.sum(b[2:m-2,2:n-2])
    #error = (after-before)/before
    #print(error)
    
#end = time.time()

#print("end")
#print(b)
#print("out")
#print(b[2:np.shape(b)[0]-2,2:np.shape(b)[1]-2])
#print("time",end-start)





















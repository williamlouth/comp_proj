import numpy as np
import copy
from numba import jit

np.set_printoptions(precision = 5,suppress = True)

multiple = 4
length = 14*multiple
width = int(length/14)
Ta = 20
kappa = 150
dist = (1/multiple)*10**(-3)
p = 0.5*10**9


@jit
def solver(input_array):
    """change to gauss siedel  = jacobi but update input matrix after each point"""
    
    m = np.shape(input_array)[0]
    n = np.shape(input_array)[1]
    #output_array = copy.copy(input_array)
    for i in range(2,m-2):
        for j in range(2,n-2):
            input_array[i][j] = 0.25*(input_array[i-1][j]+input_array[i+1][j]+input_array[i][j+1]+input_array[i][j-1]+dist**2*p*(1/kappa))
            #input_array[i][j] = 0.25*(input_array[i-1][j]+input_array[i+1][j]+input_array[i][j+1]+input_array[i][j-1])
    #input_array[2:m-2,2:n-2] = 0.25*(np.roll(input_array,1)+np.roll(input_array,-1)+
    #                     np.roll(input_array,1,axis = 0)+np.roll(input_array,-1,axis = 0)+dist**2*p*(1/kappa)*np.ones((m,n)))[2:m-2,2:n-2]        
    return input_array
    



def derivatives_maker(input_array):
    m = np.shape(input_array)[0]
    n = np.shape(input_array)[1]
    input_array[2:m-2,0] = 1.31 * (input_array[2:m-2,2]-Ta)**(4/3)/kappa
    input_array[2:m-2,n-1] = 1.31 *(input_array[2:m-2,n-3]-Ta)**(4/3)/kappa
    input_array[0,2:n-2] = 1.31*(input_array[2,2:n-2]-Ta)**(4/3)/kappa
    input_array[m-1,2:n-2] = 1.31*(input_array[m-3,2:n-2]-Ta)**(4/3)/kappa
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


def imag_point_maker(input_array):
    m = np.shape(input_array)[0]
    n = np.shape(input_array)[1]
    input_array[2:m-2,1] = input_array[2:m-2,3] - 2*dist*input_array[2:m-2,0]
    input_array[2:m-2,n-2] = input_array[2:m-2,n-4] - 2*dist*input_array[2:m-2,n-1]
    input_array[1,2:n-2] = input_array[3,2:n-2] - 2*dist*input_array[0,2:n-2]
    input_array[m-2,2:n-2] = input_array[m-4,2:n-2] - 2*dist*input_array[m-1,2:n-2]   
    return input_array
    


b = np.ones((length+4,width+4))*40
#a[3,3] = 30
#a[3,4] = 40
#print("a")
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
    
    
before = 1
after = 1
error = 100
while np.abs(error) > 1e-7:
    m = np.shape(b)[0]
    n = np.shape(b)[1]
    before = copy.copy(after)
    b = derivatives_maker(b)
    b = imag_point_maker(b)
    b = solver(b)
    after = np.sum(b[2:m-2,2:n-2])
    error = (after-before)/before
    print(error)
    

print("end")
print(b)
print("out")
print(b[2:np.shape(b)[0]-2,2:np.shape(b)[1]-2])






















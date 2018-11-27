import numpy as np


np.set_printoptions(precision = 5,suppress = True)
 
p = 0.5*10**9
#p = 0
density = 15  #must be int >1
points_across = 14*density
points_up = points_across/14
dist = 14*10**(-3)/points_across
#print(points_across,points_up,dist)
kappa = 15
Ta = 20
h = 1
def run_once(intput_array):
    initial = intput_array
    m = np.shape(intput_array)[0]
    n = np.shape(intput_array)[1]
    second = np.zeros((m,n))
    for i in range(n):
        second[0][i] = initial[0][i]
        second[m-1][i] = initial[m-1][i]
    for i in range(m):
        second[i][0] = initial[i][0]
        second[i][n-1] = initial[i][n-1]
    for i in range(1,m-1):
        for j in range(1,n-1):
            second[i][j] = 0.25 *(initial[i-1][j]+initial[i+1][j]+initial[i][j-1]+initial[i][j+1]) + (1.0/kappa)*(dist**2*p*0.25) #add cooling term here?
    #second[1][1] = 0.5*(initial[2][1]+initial[1][2]) + (dist**2*p/kappa*0.25)
    #second[1][n-2] = 0.5*(initial[2][n-2]+initial[1][n-3]) + (dist**2*p/kappa*0.25)
    #second[m-2][1] = 0.5*(initial[m-3][1]+initial[m-2][2]) + (dist**2*p/kappa*0.25)
    #second[m-2][n-2] = 0.5*(initial[m-3][n-2]+initial[m-2][n-3]) + (dist**2*p/kappa*0.25)
    return second 
        




def imag_points(input_array,derivatives):
    m = np.shape(input_array)[0]
    n = np.shape(input_array)[1]
    output = np.zeros((m+2,n+2))
    #print("anna")
    #print(input_array)
    for i in range(n):
        output[0][i+1] = input_array[1][i] - 2*dist*derivatives[0][i+1]
        output[m+1][i+1] = input_array[m-2][i]- 2*dist*derivatives[m+1][i+1]
    for i in range(m):
        output[i+1][0] = input_array[i][1]- 2*dist*derivatives[i+1][0]
        output[i+1][n+1] = input_array[i][n-2]- 2*dist*derivatives[i+1][n+1]
    #print("bob")
    #print(output)
    return output


def derivative_cal(input_array):
    m = np.shape(input_array)[0]
    n = np.shape(input_array)[1]
    output = np.zeros((m+2,n+2))
    for i in range(n):
        h = 1.31 *np.cbrt(np.abs((input_array[0][i]-Ta)))
        output[0][i+1] = (input_array[0][i]-Ta)*h
        h = 1.31 *np.cbrt(np.abs((input_array[m-1][i]-Ta)))
        output[m+1][i+1] = (input_array[m-1][i]-Ta)*h
    for i in range(m):
        h = 1.31 *np.cbrt(np.abs((input_array[i][0]-Ta)))
        output[i+1][0] = (input_array[i][0]-Ta)*h
        h = 1.31 *np.cbrt(np.abs((input_array[i][n-1]-Ta)))
        output[i+1][n+1] = (input_array[i][n-1]-Ta)*h
        
    #print("hi")
    #print(output)
    return output

def run_func(input_array):
    m = np.shape(input_array)[0]
    n = np.shape(input_array)[1]
    mid_vals = input_array
    derivatives = derivative_cal(mid_vals)
    
    imags = imag_points(mid_vals,derivatives)
    mid_vals = np.pad(mid_vals,1,mode = 'constant')
    to_test = mid_vals+imags
    #print("yo")
    #print(to_test)
    for i in range(5):
       # print("h",to_test)
        to_test = run_once(to_test)
        
    return to_test[1:m+1,1:n+1] 



initialise_array = np.ones((int(points_across),int(points_up)))*20
b = initialise_array
for i in range(5000):
    b = run_func(b)
print("b")
print(b)
print((1*dist**2*p/kappa*0.25),"power per point ish")
print(dist)
print(points_across,points_up)











































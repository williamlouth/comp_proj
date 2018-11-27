import numpy as np



 
p = 5.5
dist = 0.05
kappa = -0.5

def run_once(intput_array):
    initial = intput_array
    m = np.shape(intput_array)[0]
    n = np.shape(intput_array)[1]
    second = np.zeros((m,n))
    for i in range(m):
        second[0][i] = initial[0][i]
        second[n-1][i] = initial[n-1][i]
    for i in range(n):
        second[i][0] = initial[i][0]
        second[i][m-1] = initial[i][m-1]
    for i in range(1,m-1):
        for j in range(1,n-1):
            second[i][j] = 0.25 *(initial[i-1][j]+initial[i+1][j]+initial[i][j-1]+initial[i][j+1]) - (dist**2*p/kappa*0.25)
    return second 
        
a = np.ones((40,40))

a[1][2] = 2.2
a[2][2] = 4.4

print(a)    
print(run_once(a))


b = run_once(a)

for i in range(1000):
    b = run_once(b)
    print(b)






















































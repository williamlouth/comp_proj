import numpy as np
import copy
from numba import jit
import time
import pylab as pl





class block:
    omega = 1.75
    def __init__(self,initial_array,kappa,tot_power,dist):
        print("here")
        self.points = np.pad(initial_array,1,mode = 'constant',constant_values = 0)
        self.kappa = kappa
        self.dist = dist
        self.tot_power = tot_power

        self.top_type = np.zeros(self.points.shape[0])
        self.bot_type = np.zeros(self.points.shape[0])
        

    def edge_maker(self):
        print("hi")


    def solver(input_array,tot_power):
        m = self.points.shape[0]
        n = self.points.shape[1]
        for i in range(1,m-1):
            for j in range(1,n-1):
                self.points[i][j] = self.points[i][j]*(1-omega) + omega*0.25*(self.points[i-1][j]+self.points[i+1][j]+self.points[i][j+1]+self.points[i][j-1]+self.dist**2*self.tot_power*(1/self.kapp))
        return self.points
 
    #points = np.array((width,height))    
    #shape = points.shape
    #kappa = 
    #boundary = 
    ##need to store location of object that holds other temps
    
    
    
    


bob = block(np.array([[1,2],[3,4]]))
print(bob.points)


































































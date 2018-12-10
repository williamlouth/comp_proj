import numpy as np
import numba
from numba import int32,float64
from numba import jitclass

from numba import deferred_type,optional


print(numba.__version__)
test_type = deferred_type()
spec = [('m',int32),('tom',float64[:,:])]
@jitclass(spec)
class bob:
    def __init__(self,input1):
        self.tom = input1
        self.m = self.tom.shape[0]
        print(self.m)




test_type.define(bob.class_type.instance_type)


a = np.array([[1,2],[3,4]])
print(a)
b = np.array([[4,6],[9,8]])
print(b)
c= np.append([a],[b],axis=0)
print(c)
d=[a,b]
print(d)

e = np.array([i for i in d])
print(e)
print(e[1,1,1])

print(c[1,1,1])


bib = bob(np.ones((2,2)))



































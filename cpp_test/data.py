import numpy as np
import pylab as pl








max_temps =[]

for i in range(5,31,5):
    a = np.genfromtxt(str(i),delimiter=',')
    a = a[:,:-1]
    #print(a)
    #a= np.ma.masked_where(a < 30,a)
    max_temps.append(np.max(a))


print(max_temps)



#pl.imshow(a)
#pl.show()

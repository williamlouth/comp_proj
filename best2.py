import numpy as np
import copy
from numba import jit
from numba import prange
from numba import void
from numba import jitclass
from numba import int32,float64
from numba import int64
from numba import deferred_type,optional
import time
import pylab as pl
import numba

#import block
#from hello import say_hello_to

np.set_printoptions(precision = 5,suppress = True)
print(numba.__version__)

Ta = 20
omega = 1.2

@jit(nopython = True)
def solver(input_array,tot_power,kappa,dist):
    m = input_array.shape[0]
    n = input_array.shape[1]
    for i in range(1,m-1):
        for j in range(1,n-1):
            input_array[i][j] = input_array[i][j]*(1-omega) + omega*0.25*(input_array[i-1][j]+input_array[i+1][j]+input_array[i][j+1]+input_array[i][j-1]+dist**2*tot_power*(1/kappa))
 
@jit(nopython=True)
def edge_maker(points,m,n,dist,kappa,top_type,bot_type,list_of_edges_top,list_of_edges_bot):
    #print(list_of_edges)
    #points[1:m-1,0] = points[1:m-1,2] - 2*dist* 1.31 * (np.abs(points[1:m-1,1]-Ta))**(4/3)/kappa   
    points[1:m-1,0] = points[1:m-1,2] - 2*dist* 1.31 * (np.abs(points[1:m-1,1]-Ta))**(4/3)/kappa   
         
    points[1:m-1,n-1] = points[1:m-1,n-3] - 2*dist* 1.31 * (np.abs(points[1:m-1,n-2]-Ta))**(4/3)/kappa   


    points[0,1:n-1] = [points[2,a] - 2*dist*1.31*(np.abs(points[1,a]-Ta))**(4/3)/kappa if  top_type[0,a] == 0 else  list_of_edges_bot[int(top_type[0][a])-1][int(top_type[1][a])] for a in range(1,n-1)]

    points[m-1,1:n-1] = [points[m-3,a] - 2*dist*1.31*(np.abs(points[m-2,a]-Ta))**(4/3)/kappa if bot_type[0,a] == 0 else list_of_edges_top[int(bot_type[0][a])-1][int(bot_type[1][a])] for a in range(1,n-1)]

#    points[0,1:n-1] = [points[2,a] - 2*dist*1.31*(np.abs(points[1,a]-Ta))**(4/3)/kappa  for a in range(1,n-1)]
#
#    points[m-1,1:n-1] = [points[m-3,a] - 2*dist*1.31*(np.abs(points[m-2,a]-Ta))**(4/3)/kappa  for a in range(1,n-1)]
    #for j in range(1,n-1):
    #    if top_type[0][j] == 0:
    #        points[0,j] = points[2,j] - 2*dist*1.31*(np.abs(points[1,j]-Ta))**(4/3)/kappa
    #    else:
    #        points[0,j] = list_of_edges_bot[int(top_type[0][j])-1][int(top_type[1][j])]
    #    if bot_type[0][j] == 0:
    #        points[m-1,j] = points[m-3,j] - 2*dist*1.31*(np.abs(points[m-2,j]-Ta))**(4/3)/kappa
    #    else:
    #        points[m-1,j] = list_of_edges_top[int(bot_type[0][j])-1][int(bot_type[1][j])]
    #print("returning")
test_type = deferred_type()
spec = [('m',int64),('n',int64),('kappa',float64),('dist',float64),('tot_power',float64),('points',float64[:,:]),('top_type',float64[:,:]),('bot_type',float64[:,:]),('other_blocks',optional(test_type)[:])]
#numba.types.List


#@jitclass(spec)
class block:
    #@void(float64[:,:],float64,float64,float64)
    def __init__(self,initial_array,kappa,tot_power,dist):
        #print("here")
        #self.points = np.pad(initial_array,1,mode = 'constant',constant_values = 0)
        self.points = np.array(initial_array,dtype = np.float64)
        self.m = self.points.shape[0]
        self.n = self.points.shape[1]

        self.kappa = kappa
        self.tot_power = tot_power
        self.dist = dist

        self.top_type = np.zeros((2,self.n),dtype=np.float64)
        self.bot_type = np.zeros((2,self.n),dtype=np.float64)
        #print(self.top_type)
        
        #self.outside_points = np.empty(self.m*2+self.n*2)
        #self.other_blocks = np.empty((100),dtype=test_type)
        self.other_blocks =[0] 
    def type_change(self,block,block_start_index,block_end_index,points_start,points_end,top_or_bot):
        self.other_blocks.append(block)
        #print(block_start_index)
        #print(block_end_index)
        if top_or_bot == "top":
            self.top_type[0][points_start:points_end+1] = len(self.other_blocks)-1
            self.top_type[1][points_start:points_end+1] = range(block_start_index,block_end_index+1)
        if top_or_bot == "bot":
            self.bot_type[0][points_start:points_end+1] = len(self.other_blocks)-1
            self.bot_type[1][points_start:points_end+1] = range(block_start_index,block_end_index+1)


#test_type.define(block.class_type.instance_type)

    #def edge_maker(self):
    #    self.points[1:self.m-1,0] = self.points[1:self.m-1,2] - 2*self.dist* 1.31 * (np.abs(self.points[1:self.m-1,1]-Ta))**(4/3)/self.kappa   
    #     
    #    self.points[1:self.m-1,self.n-1] = self.points[1:self.m-1,self.n-3] - 2*self.dist* 1.31 * (np.abs(self.points[1:self.m-1,self.n-2]-Ta))**(4/3)/self.kappa   

    #    self.points[0,1:self.n-1] = [self.points[2,a] - 2*self.dist*1.31*(np.abs(self.points[1,a]-Ta))**(4/3)/self.kappa if  self.top_type[0,a] == 0 else  self.other_blocks[int(self.top_type[0][a])].points[-2,int(self.top_type[1][a])]for a in range(1,self.n-1)   ]

    #    self.points[self.m-1,1:self.n-1] = [self.points[self.m-3,a] - 2*self.dist*1.31*(np.abs(self.points[self.m-2,a]-Ta))**(4/3)/self.kappa if self.bot_type[0,a] == 0 else self.other_blocks[int(self.bot_type[0][a])].points[1,int(self.bot_type[1][a])] for a in range(1,self.n-1)]
        #for j in range(1,self.n-1):
        #    #if self.top_type[0][j] == 0:
        #    #    self.points[0,j] = self.points[2,j] - 2*self.dist*1.31*(np.abs(self.points[1,j]-Ta))**(4/3)/self.kappa
        #    #if self.top_type[0][j] != 0:
        #    #    self.points[0,j] = self.other_blocks[int(self.top_type[0][j])].points[-2,int(self.top_type[1][j])]
        #    
        #    if self.bot_type[0][j] == 0:
        #        self.points[self.m-1,j] = self.points[self.m-3,j] - 2*self.dist*1.31*(np.abs(self.points[self.m-2,j]-Ta))**(4/3)/self.kappa
        #    if self.bot_type[0][j] != 0:
        #        self.points[self.m-1,j] = self.other_blocks[int(self.bot_type[0][j])].points[1,int(self.bot_type[1][j])]


 
        #points = np.array((width,height))    
    #shape = points.shape
    #kappa = 
    #boundary = 
    ##need to store location of object that holds other temps
    


multiple = 3
dist = (1.0/multiple)*10**(-3)
p = 0.5*10**9

height_a =copy.copy(multiple)
width_a = multiple*14
height_b = multiple*2
width_b = multiple*20

wfmm = 2
hfmm = 30
sfmm = 8
number_f = 5

width_f = wfmm*multiple
height_f = hfmm*multiple
seperation_f = sfmm*multiple

height_c = multiple*4
width_c = (width_f * number_f) + (seperation_f*(number_f-1))

if width_c<width_b:
    print("error width c < width b")
    quit()

print(height_a,width_a)
print(height_b,width_b)
print(height_c,width_c)


stop_error = 1e-5
#stop_error = (1e-7/4014) *((height_a*width_a)+(height_b*width_b)+(height_c*width_c))
#stop_error = (1e-7)/(1e2) *((height_a*width_a))
print("stop error" , stop_error)


#a = block(np.pad(np.ones((height_a,width_a)),1,mode = 'constant',constant_values = 0)*30,150,0,dist)
a = block(np.pad(np.ones((height_a,width_a)),1,mode = 'constant',constant_values = 0)*30,150,p,dist)
b = block(np.pad(np.ones((height_b,width_b)),1,mode = 'constant',constant_values = 0)*30,230,0,dist)
c = block(np.pad(np.ones((height_c,width_c)),1,mode = 'constant',constant_values = 0)*30,248,0,dist)


#b = block(np.ones((height_b,width_b))*30,230,0,dist)
#c = block(np.ones((height_c,width_c))*30,248,0,dist)

list_of_fins = []
for i in range(number_f):
    #list_of_fins.append(block(np.ones((height_f,width_f))*30,248,0,dist))
    list_of_fins.append(block(np.pad(np.ones((height_f,width_f)),1,mode = 'constant',constant_values = 0)*30,248,0,dist))
#bob = block(np.ones((2,3))*30,200,0,int(1e-3))
#print(bob.points)
#bob.edge_maker()
#print(bob.points)
#print(bob.outside_points)
#print("a")
#print(a.points)
#print("b")
#print(b.points)
#print("c")
#print(c.points)


a.type_change(b,int((b.n-a.n)/2)+1,int((b.n+a.n)/2)-2,1,a.n-2,"top")
b.type_change(a,1,a.n-2,int((b.n-a.n)/2)+1,int((b.n+a.n)/2)-2,"bot")

b.type_change(c,int((c.n-b.n)/2)+1,int((c.n+b.n)/2)-2,1,b.n-2,"top")
c.type_change(b,1,b.n-2,int((c.n-b.n)/2)+1,int((c.n+b.n)/2)-2,"bot")
for i in range(len(list_of_fins)):
    list_of_fins[i].type_change(c,1+(width_f+seperation_f)*i,((width_f+seperation_f)*i)+width_f,1,list_of_fins[i].n-2,"bot")
    c.type_change(list_of_fins[i],1,list_of_fins[i].n-2,(width_f+seperation_f)*i,(width_f+seperation_f)*(i)+width_f-1,"top")
#print("b")
#print(b.points)
#print("c")
#print(c.points)


#for i in range(200000):
start = time.time()
print("starting computing")

def one_iteration():
    edge_maker(a.points,a.m,a.n,a.dist,a.kappa,a.top_type,a.bot_type,([x.points[1,:]for x in a.other_blocks[1:]]),([x.points[-2,:]for x in a.other_blocks[1:]]))
#    edge_maker(a.points,a.m,a.n,a.dist,a.kappa,a.top_type,a.bot_type,[0],[0])
    
    solver(a.points,a.tot_power,a.kappa,a.dist)

    edge_maker(b.points,b.m,b.n,b.dist,b.kappa,b.top_type,b.bot_type,([x.points[1,:]for x in b.other_blocks[1:]]),([x.points[-2,:]for x in b.other_blocks[1:]]))
    solver(b.points,b.tot_power,b.kappa,b.dist)
        #b.solver(omega)
        
        #c.edge_maker()
    edge_maker(c.points,c.m,c.n,c.dist,c.kappa,c.top_type,c.bot_type,([x.points[1,:]for x in c.other_blocks[1:]]),([x.points[-2,:]for x in c.other_blocks[1:]]))
    solver(c.points,c.tot_power,c.kappa,c.dist)
        #c.solver(omega)
        
    for i in list_of_fins:
            #i.edge_maker()
        edge_maker(i.points,i.m,i.n,i.dist,i.kappa,i.top_type,i.bot_type,([x.points[1,:]for x in i.other_blocks[1:]]),([x.points[-2,:]for x in i.other_blocks[1:]]))
        solver(i.points,i.tot_power,i.kappa,i.dist)



def running_func():
    before = 1
    after = 1
    error = 1
    the_count = 0
    for i in range(1000):
        one_iteration()
        print(i)
        the_count +=1
        #a.edge_maker()
        #edge_maker(a.points,a.m,a.n,a.dist,a.kappa,a.top_type,a.bot_type,[np.append(x.points[1,:]+x.points[-2,:] ) for x in a.other_blocks])
        #solver(a.points,a.tot_power,a.kappa,a.dist)
        ##a.solver(omega)
    
        #b.edge_maker()
        #solver(b.points,b.tot_power,b.kappa,b.dist)
        ##a.solver(omega)
        #
        #c.edge_maker()
        #solver(c.points,c.tot_power,c.kappa,c.dist)
        ##c.solver(omega)
        #
        #for i in list_of_fins:
        #    i.edge_maker()
        #    solver(i.points,i.tot_power,i.kappa,i.dist)
        #   #i.solver(omega)
    
# =============================================================================
#     i = 1
#     the_count = 0
#     while np.abs(error) > stop_error:
#         the_count +=1
#         before = copy.copy(after)
#         i+=1
#         if(i>1000):
#             i=1
#             print(error)
#         #a.edge_maker()
#                     #i.solver(omega)
#         one_iteration()
#         after = np.sum(a.points[1:-1,1:-1])+np.sum(b.points[1:-1,1:-1])+np.sum(c.points[1:-1,1:-1])
# #        after = np.sum(a.points[1:-1,1:-1])
#         error = (after-before)/before
# =============================================================================
        #print(error)
    print("the count", the_count)
    print("error",error)

running_func()
end = time.time()
print("computing finished")
print("time",end-start)



#print("a")
#print(a.points)
#
#print("b")
#print(b.points)
#
#print("c")
#print(c.points)

output = np.zeros((height_a+height_b+height_c+height_f,width_c))

for i in range(len(list_of_fins)):
    output[0:height_f,(width_f+seperation_f)*i:((width_f+seperation_f)*i)+width_f] = list_of_fins[i].points[1:list_of_fins[i].m-1,1:list_of_fins[i].n-1]
output[height_f:height_f+height_c,:] = c.points[1:c.m-1,1:c.n-1]
output[height_f+height_c:height_f+height_c+height_b,int((c.n-b.n)/2)+1:int((c.n+b.n)/2)-1] = b.points[1:b.m-1,1:b.n-1]
output[-height_a:,int((c.n-a.n)/2)+1:int((c.n+a.n)/2)-1] = a.points[1:a.m-1,1:a.n-1]
#output = a.points[1:a.m-1,1:a.n-1]
print(output)
print("max temp",np.max(a.points))
output = np.ma.masked_where(output <20,output)
pl.figure(1)
heatmap = pl.imshow(output)
pl.show()
pl.imsave('heatmap.png',output)
print(a.points.shape)
print(b.points.shape)
print(c.points.shape)
print(width_c)

np.savetxt("a.csv", a.points, delimiter=",")
np.savetxt("b.csv", b.points, delimiter=",")
np.savetxt("c.csv", c.points, delimiter=",")
np.savetxt("f1.csv", list_of_fins[0].points, delimiter=",")


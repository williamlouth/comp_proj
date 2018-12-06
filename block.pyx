import numpy as np
cimport numpy as np

DTYPE = np.float

ctypedef np.float64_t DTYPE_t

Ta = 20.0
cdef class block:
    cdef public int m
    cdef public int n
    cdef public np.ndarray points
    cdef public float kappa
    cdef public float dist
    cdef public float tot_power
    cdef public np.ndarray top_type
    cdef public np.ndarray bot_type
    cdef public list other_blocks

    def __init__(self,initial_array,kappa,tot_power,dist):
        #assert initial_array.dtype == np.array
        #print("here")
        self.points = np.pad(initial_array,1,mode = 'constant',constant_values = 0)
        self.m = self.points.shape[0]
        self.n = self.points.shape[1]

        self.kappa = kappa
        self.dist = dist
        self.tot_power = tot_power

        self.top_type = np.zeros((2,self.n))
        self.bot_type = np.zeros((2,self.n))
        #print(self.top_type)
        
        #self.outside_points = np.empty(self.m*2+self.n*2)
        self.other_blocks = [0]
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



    def solver(self,np.float64_t omega):
        
        cdef np.float64_t[:,:] points_view = self.points
        cdef int i
        cdef int j
        #print(self.points.dtype)
        #m = self.points.shape[0]
        #n = self.points.shape[1]
        for i in range(1,self.m-1):
            for j in range(1,self.n-1):
                points_view[i][j] = points_view[i][j]*(1-omega) + omega*0.25*(points_view[i-1][j]+points_view[i+1][j]+points_view[i][j+1]+points_view[i][j-1]+self.dist**2*self.tot_power*(1/self.kappa))
 

    def edge_maker(self):
        cdef np.float64_t[:,:] points_view = self.points
        cdef np.float64_t[:,:] top_type_view = self.top_type
        cdef np.float64_t[:,:] bot_type_view = self.bot_type
        cdef int j
        self.points[1:self.m-1,0] = self.points[1:self.m-1,2] - 2*self.dist* 1.31 * (np.abs(self.points[1:self.m-1,1]-Ta))**(4/3)/self.kappa   
        
        self.points[1:self.m-1,self.n-1] = self.points[1:self.m-1,self.n-3] - 2*self.dist* 1.31 * (np.abs(self.points[1:self.m-1,self.n-2]-Ta))**(4/3)/self.kappa   

        #for i in range(1,self.m-1):
        #    points_view[i,0] = points_view[i,2] - 2*self.dist* 1.31 * (np.abs(points_view[i,1]-Ta))**(4/3)/self.kappa   
        #    points_view[i,self.n-1] = points_view[i,self.n-3] - 2*self.dist* 1.31 * (np.abs(points_view[i,self.n-2]-Ta))**(4/3)/self.kappa   

        #self.points[0,1:self.n-1] = [self.points[2,a] - 2*self.dist*1.31*(np.abs(self.points[1,a]-Ta))**(4/3)/self.kappa if  self.top_type[0,a] == 0 else  self.other_blocks[int(self.top_type[0][a])].points[-2,int(self.top_type[1][a])]for a in range(1,self.n-1)   ]

        #self.points[self.m-1,1:self.n-1] = [self.points[self.m-3,a] - 2*self.dist*1.31*(np.abs(self.points[self.m-2,a]-Ta))**(4/3)/self.kappa if self.bot_type[0,a] == 0 else self.other_blocks[int(self.bot_type[0][a])].points[1,int(self.bot_type[1][a])] for a in range(1,self.n-1)]
        for j in range(1,self.n-1):
            if top_type_view[0][j] == 0:
                points_view[0,j] = points_view[2,j] - 2*self.dist*1.31*(np.abs(points_view[1,j]-Ta))**(4/3)/self.kappa
            else:
                points_view[0,j] = self.other_blocks[int(self.top_type[0][j])].points[-2,int(self.top_type[1][j])]
            
            if bot_type_view[0][j] == 0:
                points_view[self.m-1,j] = points_view[self.m-3,j] - 2*self.dist*1.31*(np.abs(points_view[self.m-2,j]-Ta))**(4/3)/self.kappa
            else:
                points_view[self.m-1,j] = self.other_blocks[int(self.bot_type[0][j])].points[1,int(self.bot_type[1][j])]
        return



# 
# diseaseSim.py - simulates the spread of disease through a population
#
# Student Name   : 
# Student Number :
#
# Version history:
#
# 25/4/19 - beta version released for FOP assignment
#
import numpy as np
import matplotlib.pyplot as plt
import random

random.seed(2)

# # # # # # # # # # # # # # # # # # # # # # #
# # --------- PARAMETER SETTINGS -------- # #
# # # # # # # # # # # # # # # # # # # # # # #
INIT_PPL = 10
INIT_INFCT = 2
SIZE_X = 10
SIZE_Y = 10
NEIGHB = 0      # 0: Moore neighbourhoods, 1: Von Neumann neighbourhoods
BARRIER_VER_X = -1      # location of the vertical barrier. set to -1 to disable
BARRIER_HOR_Y = -1      # location of the horizontal barrier. set to -1 to disable

# # # # # # # # # # # # # # # # # # # # # # # # # #
# # --------- FUNCTIONS AND CLASSES ---------- # # 
# # # # # # # # # # # # # # # # # # # # # # # # # #
def initWorld():
    world = []
    for y in range(SIZE_Y-1, -1, -1):
        row = []
        for x in range(0, SIZE_X):
            row.append(Grid(x, y))
        world.append(row)
    return world

def plotGrid(world):
    pass
class Grid():
    '''
    
    '''
    def __init__(self, x, y):
        self.pos = np.array([x, y])
        self.state = "safe"
    
    def toHazard(self):
        self.state = "hazard"
    
    def __repr__(self):
        '''
        
        '''
        return str(self.pos)
        
#        if self.state == "safe":
#            return 0
#        if self.state == "hazard":
#            return 1


class People():
    '''
    
    '''
    def __init__(self, x, y, status):
        self.x = x
        self.y = y
        self.pos = np.array([x, y])
        self.status = status
    def move(self, NEIGHB):
        '''
        Move the people according to Moore or Von Neumann neighbourhoods.
        The moving direction is based on random function which is decoded by 
        numlock direction as follows:
            
            7 8 9
            4 5 6
            1 2 3   for Moore neighbourhoods,
        and    
              8
            4 5 6
              2     for Von Neumann neighbourhoods.
        
        The moving step is validated by updatePos() function.        
        '''
        if NEIGHB == 0: # if Moore neighbourhoods
            new_grid = np.random.choice([1,2,3,4,5,6,7,8,9])
        if NEIGHB == 1: # if Von Neumann neighbourhoods
            new_grid = np.random.choice([  2,  4,5,6,  8  ])
        
        if new_grid == 1:
            self.x += -1
            self.y += -1
        elif new_grid == 2:
            self.x += 0
            self.y += -1
        elif new_grid == 3:
            self.x += 0
            self.y += -1
        elif new_grid == 4:
            self.x += 0
            self.y += -1
        elif new_grid == 5:
            self.x += 0
            self.y += -1
        elif new_grid == 6:
            self.x += 0
            self.y += -1
        elif new_grid == 7:
            self.x += 0
            self.y += -1
        elif new_grid == 8:
            self.x += 0
            self.y += -1
        elif new_grid == 9:
            self.x += 0
            self.y += -1
            
        self.updatePos()
    def updatePos(self, x, y):
        '''
        Check whether the new step exceeds the domain of the problem or 
        clashes the barrier.
        '''
        # if x exceeds the boundary, keep it at boundary
        if x < 0:
            x = 0
        if x >= SIZE_X:
            x = SIZE_X-1
        # if y exceeds the boundary, keep it at boundary
        if y < 0:
            y = 0
        if y >= SIZE_Y:
            y = SIZE_Y-1
        # if x or y crashes the barrier, do not move
        if x == BARRIER_VER_X or y == BARRIER_HOR_Y:
            self.x = self.pos[0] # restore to previous value
            self.y = self.pos[1] # restore to previous value
        else:
            self.x = x
            self.y = y
            self.pos = np.array([x, y]) # update position
        
            
    
        
# # # # # # # # # # # # # # # # # # # # # #        
# # ----------- START HERE ------------ # #       
# # # # # # # # # # # # # # # # # # # # # #
world = initWorld()

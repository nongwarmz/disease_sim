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
np.random.seed(3)

# # # # # # # # # # # # # # # # # # # # # # #
# # --------- PARAMETER SETTINGS -------- # #
# # # # # # # # # # # # # # # # # # # # # # #
INIT_PPL = 10
INIT_INFCT = 4
SIZE_X = 5              # size of x-domain
SIZE_Y = 5              # size of y-domain
NEIGHB = 0              # 0: Moore neighbourhoods, 1: Von Neumann neighbourhoods
BARRIER_VER_X = -1      # location of the vertical barrier. set to -1 to disable
BARRIER_HOR_Y = -1      # location of the horizontal barrier. set to -1 to disable
NUM_STEPS = 10
INFCT_THRES = 0.8
CURE_THRES = 0.1
DEAD_THRES = 0.1

# # # # # # # # # # # # # # # # # # # # # # # # # #
# # --------- FUNCTIONS AND CLASSES ---------- # # 
# # # # # # # # # # # # # # # # # # # # # # # # # #
def initWorld():
    '''
    Initiate the world that contains 2d-list of Grid objects.
    '''
    world = []
    for y in range(SIZE_Y-1, -1, -1):
        row = []
        for x in range(0, SIZE_X):
            row.append(Grid(x, y))
        world.append(row)
    return world

def initPpl():
    '''
    Initiate list of People objects.
    '''
    ppl = []
    for i in range(0, INIT_PPL):
        x = BARRIER_VER_X
        y = BARRIER_HOR_Y
        while x == BARRIER_VER_X or y == BARRIER_HOR_Y:
        # This loop avoid initiation at the barrier location
            x = np.random.randint(0, SIZE_X)
            y = np.random.randint(0, SIZE_Y)
        if i < INIT_INFCT:
            ppl.append(People(x=x, y=y, status="infected"))
        else:
            ppl.append(People(x=x, y=y, status="healthy"))
    return ppl

def refreshPpl(world):
    '''
    Refresh number of People in each Grid.
    '''
    for w in world:
        for grid in w:
            grid.numPpl = 0
    return world

def updatePeopleInWorld(world, ppl):
    '''
    Count number of People in each Grid and update into Grid.numPpl.
    '''
    world = refreshPpl(world)
    for p in ppl:
        world[SIZE_Y-1 - p.pos[1]][p.pos[0]].numPpl += 1
    return world

def updateInfectPeople(ppl):
    '''
    Healthy People whowho stays in the same Grid as Infected People has a chance
    to get infected.
    '''
    for p1 in ppl:
        if p1.status == "infected":
            hazardPos = p1.pos
            for p2 in ppl:
                if (p2.pos == hazardPos).all() and p2.status != "infected":
                    prob = np.random.uniform(0,1)
                    if prob < INFCT_THRES:
                        p2.status = "infected"
                        print("People get infected at grid", hazardPos)
    return ppl
def curePeople(ppl):
    '''
    Infected People has a chance to be cured.
    '''
    for p in ppl:
        if p.status == "infected":
            prob = np.random.uniform(0,1)
            if prob < CURE_THRES:
                p.status = "healthy"
                print("People get cured at grid", p.pos)
    return ppl
def deadPeople(ppl):
    '''
    Infected People has a chance to die. Dead People are unable to be cured.
    '''
    for p in ppl:
        if p.status == "infected":
            prob = np.random.uniform(0,1)
            if prob < DEAD_THRES:
                p.status = "dead"
                print("People died at grid", p.pos)
def movePeople(ppl):
    '''
    Move list of People. If they are still alive.
    '''
    for p in ppl:
        if p.status != "dead":
            p.move()
    return ppl
def printPplStatus(ppl):
    '''
    Print status of of list of People.
    '''
    stat = []
    for p in ppl:
        stat.append(p.status)
    print(stat)
def countInfected(ppl):
    '''
    Count number of infected People.
    '''
    cnt = 0
    for p in ppl:
        if p.status == "infected":
            cnt+=1
    return cnt

class Grid():
    '''
    Grid class to represent one particular location in the world. 
    
    Attributes:
        pos (float, float) representing position of the Grid
        numPpl (int) representing number of People in this Grid
    '''
    def __init__(self, x, y):
        self.pos = np.array([x, y])
        self.numPpl = 0
       
    def __repr__(self):
        '''
        This function prints the returned value if print() is used.
        '''
        return str(self.numPpl)
    

class People():
    '''
    People class to represent one People.
    
    Attributes:
        pos (float, float) representing position of People. It is redundant to 
    x and y due to make the move method
        status (str) representing status of the People. Available choices are:
            [healthy, infected, dead]
    '''
    def __init__(self, x, y, status="healthy"):
        self.pos = np.array([x, y])
        self.status = status
    def move(self):
        '''
        Move the people according to Moore or Von Neumann neighbourhoods.
        The moving direction is based on random function which is decoded by 
        numpad direction as follows:
            
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
        
        x, y = self.pos
        if new_grid == 1:
            x += -1
            y += -1
        elif new_grid == 2:
            x +=  0
            y += -1
        elif new_grid == 3:
            x +=  1
            y += -1
        elif new_grid == 4:
            x += -1
            y +=  0
        elif new_grid == 5:
            x +=  0
            y +=  0
        elif new_grid == 6:
            x +=  1
            y +=  0
        elif new_grid == 7:
            x += -1
            y +=  1
        elif new_grid == 8:
            x +=  0
            y +=  1
        elif new_grid == 9:
            x +=  1
            y +=  1
        # check and update the new grid
        self.updatePos(x, y)
        
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
            x = self.pos[0] # restore to previous value
            y = self.pos[1] # restore to previous value
        else:
            self.pos = np.array([x, y]) # update position
    def __repr__(self):
        '''
        This function prints the returned value if print() is used.
        '''
        return str(self.pos)
            
    
        
# # # # # # # # # # # # # # # # # # # # # #        
# # ----------- START HERE ------------ # #       
# # # # # # # # # # # # # # # # # # # # # #
world = initWorld()
ppl = initPpl()
world = updatePeopleInWorld(world, ppl)
infctHist = [countInfected(ppl)]

for t in range(0, NUM_STEPS):
    print("======= Time step {} =======".format(t) )
    print("** World Map Showing how many people in each grid **")
    print(np.array(world))
    world = updatePeopleInWorld(world, ppl)   
    print("People position:")
    print(ppl) # This print shows location of each People
    print("People status:")
    printPplStatus(ppl) # This print shows the status of each People
    ppl = updateInfectPeople(ppl)
    ppl = curePeople(ppl)
    ppl = movePeople(ppl)
    infctHist.append(countInfected(ppl))

plt.plot(infctHist)
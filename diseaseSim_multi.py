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
import pandas as pd
import sys

# Keep these numbers to maintain the repeatability of the results
random.seed(2)
np.random.seed(2)

def distribute(grid, num_r, num_c, numpeep):
    for i in range(numpeep):
        rpos = BARRIER_ROW
        cpos = BARRIER_COL
        while rpos == BARRIER_ROW or cpos == BARRIER_COL:
            # this loop avoids initate people on the barrier
            rpos = random.randint(0, num_r-1)
            cpos = random.randint(0, num_c-1)
        grid[rpos, cpos] += 1
#        print("Adding 1 to (", xpos, ",", ypos,")")

def makeScatter(grid, num_r, num_c):
    r_values = []
    c_values = []
    count_values = []
    for row in range(num_r):
        for col in range(num_c):
            if grid[row,col] > 0:
                r_values.append(row)
                c_values.append(col)
                count_values.append(grid[row,col]*100)
#                print("Value at (", row, ",", col, ") is ", grid[row, col])
    return(r_values, c_values, count_values)
    
def displayGrid(grid, num_r, num_c):
    for row in range(num_r-1, -1, -1):
        for col in range(num_c):
            print(grid[row,col], end=" ")
        print()

def plotGrids():
    Irows, Icols, Icount = makeScatter(infected, NUM_ROWS, NUM_COLS)
    plt.scatter(Irows, Icols, s=Icount, c="r", alpha=0.5)
    Urows, Ucols, Ucount = makeScatter(uninfected, NUM_ROWS, NUM_COLS)
    plt.scatter(Urows, Ucols, s=Ucount, c="b", alpha=0.5)
    plt.scatter(airports[:,0], airports[:,1], c="y", marker="x", alpha=0.5)
    plt.axhline(BARRIER_COL)
    plt.axvline(BARRIER_ROW)
    plt.xlim(-1, NUM_ROWS+1)
    plt.ylim(-1, NUM_COLS+1)
    plt.show()
          
def movePeeps(cur_peeps, next_peeps, r, c):
#    print("Pos (", r, ",", c, ") has ", cur[r,c], " people")
    for peep in range(cur_peeps[r,c]):
        if NEIGHB == 0: # if Moore Neightbourhoods
            rMove = random.randint(-1,1)
            cMove = random.randint(-1,1)
        elif NEIGHB == 1: # if Von Neumann neighbourhoods
            move = random.randint(-1,1)
            direction = random.randint(0, 1)
            if direction == 0:
                rMove = move
                cMove = 0
            if direction == 1:
                rMove = 0
                cMove = move
        if (r + rMove) > (NUM_ROWS-1) or \
        (r + rMove) < 0 or \
        (r + rMove) == BARRIER_ROW :
            rMove = 0
        if (c + cMove) > (NUM_COLS-1) or \
        (c + cMove) < 0 or \
        (c + cMove) == BARRIER_COL :
            cMove = 0   
        next_peeps[r + rMove, c + cMove] +=1
    #         print("Move from (", r, ",", c, ") to (", r+rMove, "," , c+cMove, ")")

def init_airports(NUM_ROWS, NUM_COLS, NUM_AIRPORTS):
    rows = BARRIER_ROW*np.ones(NUM_AIRPORTS)
    cols = BARRIER_COL*np.ones(NUM_AIRPORTS)
    while (BARRIER_ROW in rows) or (BARRIER_COL in cols):
        rows = np.random.randint(NUM_ROWS, size=NUM_AIRPORTS)
        cols = np.random.randint(NUM_COLS, size=NUM_AIRPORTS)
    airports = np.c_[rows, cols]
    return airports
def flyPeeps(cur_peeps, next_peeps, r, c):
    cur_airport = np.array([r,c])    
    for peep in range(cur_peeps[r,c]):
        new_airport = cur_airport
        while (new_airport == cur_airport).all():
            new_airport = random.choice(airports)
        cur_peeps[r,c] -= 1
        next_peeps[new_airport[0], new_airport[1]] += 1
        print("*** Transferring from airport: ", cur_airport, " to ", new_airport)
    return next_peeps
def infect(inf, notinf, r, c, prob):
#    print("Pos (", r, ",", c, ") has ", inf[r,c], " inf people and ", notinf[r,c], " well people")
    prob = prob * inf[r,c]
    if prob:
        for peep in range(notinf[r,c]):
            if random.random() < prob:
                inf[r, c] +=1
                notinf[r, c] -=1
                print("***** New infection (", r, ",", c, ")")
    return inf, notinf
def cure(inf, notinf, r, c, prob):
    for peep in range(inf[r,c]):
        if random.random() < prob:
            notinf[r, c] +=1
            inf[r, c] -=1
            print("***** Cure infection (", r, ",", c, ")")
    return inf, notinf
def die(inf, r, c, prob):
    for peep in range(inf[r,c]):
        if random.random() < prob:
            inf[r, c] -= 1
            print("***** Infection die (", r, ",", c, ")")
    return inf

INIT_POP = int(sys.argv[1])
INIT_INFECTED = 20
NUM_COLS = 15
NUM_ROWS = 15
NUM_STEPS = 5
NEIGHB = 1
NUM_AIRPORTS = 3
BARRIER_ROW = 2
BARRIER_COL = 3
PROB_INFECT = 0.5
PROB_CURE = 0.2
PROB_DIE = 0.1
PROB_FLY = 0.3
#world = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
infected = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
uninfected = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
airports = init_airports(NUM_ROWS, NUM_COLS, NUM_AIRPORTS)

distribute(infected, NUM_ROWS, NUM_COLS, INIT_INFECTED)
distribute(uninfected, NUM_ROWS, NUM_COLS, INIT_POP)

#print(world)
#print()
displayGrid(infected, NUM_ROWS, NUM_COLS)
print()
displayGrid(uninfected, NUM_ROWS, NUM_COLS)

plotGrids()

for timestep in range(NUM_STEPS):
    print("\n###################### TIMESTEP", timestep, "#####################\n")
    infected2 = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
    uninfected2 = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            infected, uninfected = infect(infected, uninfected, row, col, PROB_INFECT)
            infected, uninfected = cure(infected, uninfected, row, col, PROB_CURE)
            infected = die(infected, row, col, PROB_DIE)
            if ([row, col] == airports).all(axis=1).any() and \
                    random.random() < PROB_FLY and \
                    len(airports) > 1:
                flyPeeps(infected, infected2, row, col)
                flyPeeps(uninfected, uninfected2, row, col)
            movePeeps(infected, infected2, row, col)
            movePeeps(uninfected, uninfected2, row, col)
    infected = infected2
    uninfected = uninfected2
#    plotGrids()
    print("Total uninfected people: ", uninfected.sum().sum())
    print("Total infected pelple: ", infected.sum().sum())

print("Done")
with open("output.txt", "a") as f:
    #text = "Initial Population: {}, Final uninfected: {}, Final infected {}\n".format(INIT_POP, uninfected.sum().sum(), infected.sum().sum())
    dead = INIT_POP+INIT_INFECTED-uninfected.sum().sum()-infected.sum().sum()
    text = "{}, {}, {}, {}, {}\n".format(INIT_POP, INIT_INFECTED, uninfected.sum().sum(), infected.sum().sum(), dead)
    f.write(text)

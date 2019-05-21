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

def distribute(grid, num_r, num_c, numpeep):
    for i in range(numpeep):
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
    plt.show()
          
def movePeeps(cur, next, r, c):
#    print("Pos (", r, ",", c, ") has ", cur[r,c], " people")
    for peep in range(cur[r,c]):
         rMove = random.randint(-1,1)
         cMove = random.randint(-1,1)
#         print("Move from (", r, ",", c, ") to (", r+rMove, "," , c+cMove, ")")
         if (r + rMove) > (NUM_ROWS-1) or (r + rMove) < 0:
             rMove = 0
         if (c + cMove) > (NUM_COLS-1) or (c + cMove) < 0:
             cMove = 0   
         next[r + rMove, c + cMove] +=1
#         print("          (", r, ",", c, ") to (", r+rMove, "," , c+cMove, ")")
    
def infect(inf, notinf, r, c, prob):
#    print("Pos (", r, ",", c, ") has ", inf[r,c], " inf people and ", notinf[r,c], " well people")
    prob = prob * inf[r,c]
    if prob:
        for peep in range(notinf[r,c]):
            if random.random() < prob:
                inf[r, c] +=1
                notinf[r, c] -=1
                print("***** New infection (", r, ",", c, ")")


INIT_POP = 100
INIT_INFECTED = 5
NUM_COLS = 15
NUM_ROWS = 10
NUM_STEPS = 10

#world = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
infected = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
uninfected = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)

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
            infect(infected, uninfected, row, col, 0.5)
            movePeeps(infected, infected2, row, col)
            movePeeps(uninfected, uninfected2, row, col)
    infected = infected2
    uninfected = uninfected2
    plotGrids()

print("Done")
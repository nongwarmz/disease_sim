import numpy as np
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

param_list = range(30, 80, 10)

if os.path.isfile("output.txt"):
    os.remove("output.txt")
with open("output.txt", "w") as f: # write header
    f.write("INIT_POP, INIT_INFECTED, uninfected, infected, dead\n")
for v in param_list:
    os.system("python diseaseSim_multi.py "+ str(v))

#with f as open("output.txt", "r"):
df = pd.read_csv("output.txt")
df.columns = df.columns.str.replace(' ', '')
# # # plot INIT_POP vs uninfected
plt.figure()
plt.plot(df['INIT_POP'], df['uninfected'])
plt.xlabel('Initial population')
plt.ylabel('Number of final uninfected people')
# # # plot INIT_POP vs infected
plt.figure()
plt.plot(df['INIT_POP'], df['infected'])
plt.xlabel('Initial population')
plt.ylabel('Number of final infected people')
# # # plot INIT_POP vs dead
plt.figure()
plt.plot(df['INIT_POP'], df['dead'])
plt.xlabel('Initial population')
plt.ylabel('Number of final dead people')
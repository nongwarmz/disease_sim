import numpy as np
import sys
import os

param_list = range(10, 600, 10)

if os.path.isfile("output.txt"):
    os.remove("output.txt")
for v in param_list:
    os.system("python diseaseSim_multi.py "+ str(v))
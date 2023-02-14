'''
THIS IS NOT TO BE USED AT THE MOMENT, USE main.py IN THE latticepy FOLDER
'''


import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../latticepy')

try:
    from tqdm import tqdm as tq
except:
    def tq(x):
        return x

# Only for GPU runs
from params import DEV
if DEV == 'gpu':
    try:
        from numba import cuda
        import cupy as cp
    except:
        raise ImportError("Need to install cupy and have an NVIDIA gpu to run!")

from field import *

import ic
import params

import utils
from prop import propagate
import plotting


# Main path
path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))


def main():
    start = time.time()
    t = 0
    field = Field()
    utils.banner()
    if field.verb != 'silent':
        utils.summary(field)

    #ic.create_ic(field)
    ic.read_jaxions(field)
    
    plotting.singleplot(field,0,channel='psi',label=True)

    field.set_k2()
    field.set_potential()

    print("Main loop ...")
    
    field.set_steps()
    field.a = 0.01
    #for i in tq(range(field.steps)):
    i = 0 
    while field.a < 2:
        propagate(field)
        if i in range(0,field.steps*100,25):
            print("%d %.5f"%(i,field.a))
        if i in range(0,field.steps,100):
            
            plotting.singleplot(field,i,channel='psi',label=True)
        i += 1
    print("Walltime: %.1f seconds "%(time.time()-start))
    #plotting.singleplot(field,i,channel='psi')
    #plotting.doubleplot_SP(field,i)
    return 0


if __name__ == "__main__":
    main()

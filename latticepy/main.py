import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

try:
    from tqdm import tqdm as tq
except:
    def tq(x):
        return x

import ic
import params 
import utils
from prop import propagate
import plotting as pl 
from field import *

if params.DEV == 'gpu':
    from numba import cuda
    import cupy as cp

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def main():
    start = time.time()

    field = Field()
    field.start_run()
    utils.banner()
    utils.summary(field)  
    
    # Create/Read Initial conditions
    if field.ictype == 'solitons':
        ic.create_ic(field)
    else:
        ic.read_ic(field) 
    
    field.set_k2()
    field.set_potential()
     
    if field.device == 'gpu':
        field.copy_to_host()
    pl.singleplot(field,0,channel='psi')
    
    field.set_steps()

    print("Main loop ...")
    for i in tq(range(field.steps)):
        propagate(field)

    if field.device == 'gpu':
        field.copy_to_host()
    pl.singleplot(field,i,channel='psi')
    print("Walltime: %.1f seconds"%(time.time()-start))
    return 0


if __name__== "__main__":
    main()



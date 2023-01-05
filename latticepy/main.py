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
import plotting
from field import *

if params.DEV == 'gpu':
    from numba import cuda
    import cupy as cp

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def main():
    start = time.time()

    field = Field()

    utils.banner()
    utils.summary(field)  

    ic.create_ic(field)
    
    # Implement flag here
    flag = False
    if flag == True:
        if field.device == 'gpu':
            field.copy_to_host()
        plotting.singleplot(field,channel='psi')
    
    field.set_k2()
    field.set_potential()
     
    Nsteps = utils.set_steps(field)

    for i in tq(range(Nsteps)):
        propagate(field)

    # Implement another flag here
    flagf = True
    if flagf == True:
        if field.device == 'gpu':
            field.copy_to_host()
        plotting.singleplot(field,channel='psi')

    print("Walltime: %.1f seconds"%(time.time()-start))
    return 0


if __name__== "__main__":
    main()



import matplotlib.pyplot as plt
import cmasher as cmr
import numpy as np

# Some utility functions

def banner():
    print("++++++++++++++++++++++++++++++")
    print("        LatticePy (2023)      ")
    print("++++++++++++++++++++++++++++++")

def summary(f):
    if f.verb == 'silent':
        pass
    elif f.verb == 'normal' or f.verb == 'debug':
        print("Gridsize  = %d"%f.Ngrid)
        print("Dimension = %d"%f.ndims)
        print("Device    = %s"%f.device)
        print("Precision = %s"%f.prec)
        print("IC type   = %s"%f.ictype)
        print("Boxsize   = %d"%f.boxsize)
        print("Timestep  = %.4f"%f.dt)

def set_steps(field):
    steps = int(np.ceil(field.tf/field.dt))
    if field.verb != 'silent':
        print("Loop will take %d steps"%steps)
    return steps

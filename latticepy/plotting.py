import os
import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

def set_plot_pars():
    plt.rcParams['axes.linewidth'] = 2
    #plt.rc('text', usetex=True)
    plt.rc('font', family='serif',size=15)

def singleplot(field,index,channel='psi',label=False):
    set_plot_pars()
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    if channel =='psi':
        if field.ndims == 2:
            im = ax.imshow(np.log10(np.abs(field.psi)**2),cmap=cmr.eclipse,extent=[0,field.boxsize,0,field.boxsize],vmin=-2,vmax=2)
        elif field.ndims == 3:
            im = ax.imshow(np.log10(np.mean(np.abs(field.psi)**2,axis=2)),cmap=cmr.eclipse,extent=[0,field.boxsize,0,field.boxsize])
    elif channel == 'phase':
        if field.ndims == 2:
            im = ax.imshow(np.angle(field.psi),cmap=cmr.copper_s,extent=[0,field.boxsize,0,field.boxsize])
        elif field.ndims == 3:
            im = ax.imshow(np.angle(field.psi[np.random.randint(field.Ngrid)]),cmap=cmr.copper_s,extent=[0,field.boxsize,0,field.boxsize])
    elif channel == 'gravpot':
        pass
    plt.colorbar(im)
    if label == True:
        ax.set_xlabel(r"$x/L$",fontsize=20)
        ax.set_ylabel(r"$y/L$",fontsize=20)
    else:
        ax.set_xticks([])
        ax.set_yticks([])
    fig.savefig(field.sdir+'/plots/ps_%s_%d.png'%(channel,index),bbox_inches='tight')
    #fig.savefig('/home/z5278074/lpy_simple/ps_%s_%d.png'%(channel,index),bbox_inches='tight')



def doubleplot_SP(field,index):
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(10,10))
    if field.ndims == 2:
        im1 = ax1.imshow(np.log10(np.abs(field.psi)**2),cmap=cmr.eclipse,extent=[0,field.boxsize,0,field.boxsize],vmin=-2,vmax=2)
        im2 = ax2.imshow(np.angle(field.psi),cmap=cmr.copper_s,extent=[0,field.boxsize,0,field.boxsize])
    elif NDIMS == 3:
        ax1.imshow(np.log10(np.mean(np.abs(psi)**2,axis=0)), cmap = 'inferno')
        ax2.imshow(np.angle(psi[0]), cmap = 'twilight')
    ax1.set_title(r'$\log_{10}(|\psi|^2)$')
    ax2.set_title(r'${\rm angle}(\psi)$')
    #fig.savefig('/home/z5278074/lpy_simple/doubleSP_%d.png'%(index),bbox_inches='tight')

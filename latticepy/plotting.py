import os
import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def set_plot_pars():
    pass

def singleplot(field,channel='psi'):
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    if channel =='psi':
        if field.ndims == 2:
            ax.imshow(np.log10(np.abs(field.psi)**2),cmap=cmr.eclipse,extent=[0,field.boxsize,0,field.boxsize])
        elif field.ndims == 3:
            ax.imshow(np.log10(np.mean(np.abs(field.psi)**2,axis=2)),cmap=cmr.eclipse,extent=[0,field.boxsize,0,field.boxsize])
    elif channel == 'phase':
        if field.ndims == 2:
            ax.imshow(np.angle(field.psi),cmap=cmr.copper_s,extent=[0,field.boxsize,0,field.boxsize])
        elif field.ndims == 3:
            ax.imshow(np.angle(field.psi[np.random.randint(field.Ngrid)]),cmap=cmr.copper_s,extent=[0,field.boxsize,0,field.boxsize])
    elif channel == 'gravpot':
        pass
    fig.savefig(path+'/tests/plots/ps_%s.png'%(channel),bbox_inches='tight')


'''
def doubleplot_SP(field):
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(10,10))
    if NDIMS == 2:
        ax1.imshow(np.log10(np.abs(psi)**2), cmap = 'inferno')
        ax2.imshow(np.angle(psi), cmap = 'twilight')
    elif NDIMS == 3:
        ax1.imshow(np.log10(np.mean(np.abs(psi)**2,axis=0)), cmap = 'inferno')
        ax2.imshow(np.angle(psi[0]), cmap = 'twilight')
    ax1.set_title(r'$\log_{10}(|\psi|^2)$')
    ax2.set_title(r'${\rm angle}(\psi)$')
    plt.show()

'''

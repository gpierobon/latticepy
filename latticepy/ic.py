import os
import time
import numpy as np

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

'''
def random(NDIMS,DEV):
    return 

def solitons_random(NDIMS,DEV,NSOL):
    for i in range(NSOL):
        if DEV == 'cpu':
            if NDIMS == 2:
                #write here
            elif NDIMS === 3:
                #write here
            
        elif DEV == 'gpu':
            import cupy as cp
            if NDIMS == 2:
                #write here
            elif NDIMS == 3:
                #write here
    return 
'''

def solitons_file(field):
    rho = 0.5
    path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    lines = np.loadtxt('%s/files/%s'%(path,field.icfile))

    amp_l = []; sig_l = [] 
    xc = []; yc = []; zc = []
    for line in lines:
        amp_l.append(line[0])
        sig_l.append(line[1])
        xc.append(line[2])
        yc.append(line[3])
        if field.ndims == 3:
            zc.append(line[4])
    field.create_Grid()
    xx = field.xx 
    yy = field.yy 
    zz = field.zz
    for i in range(len(lines)):
        if field.device == 'cpu':
            if field.ndims == 2:
                rho += amp_l[i]*np.exp(-((xx-xc[i])**2+(yy-yc[i])**2)/2/sig_l[i]**2)/(sig_l[i]**3*np.sqrt(2*np.pi)**2)
            elif field.ndims == 3:
                rho += amp_l[i]*np.exp(-((xx-xc[i])**2+(yy-yc[i])**2+(zz-zc[i])**2)/2/sig_l[i]**2)/(sig_l[i]**3*np.sqrt(2*np.pi)**2)
            if field.prec == 'single':
                field.psi = np.sqrt(rho/np.mean(rho)).astype('complex64')
        elif field.device == 'gpu':
            import cupy as cp
            if field.ndims == 2:
                rho = cp.add(rho,amp_l[i]*np.exp(-((xx-xc[i])**2+(yy-yc[i])**2)/2/sig_l[i]**2)/(sig_l[i]**3*np.sqrt(2*np.pi)**2))
            elif field.ndims == 3:
                rho = cp.add(rho,amp_l[i]*np.exp(-((xx-xc[i])**2+(yy-yc[i])**2+(zz-zc[i])**2)/2/sig_l[i]**2)/(sig_l[i]**3*np.sqrt(2*np.pi)**2))
            if field.prec == 'single':
                field.psi_d = cp.sqrt(rho/cp.mean(rho)).astype('complex64')
    del rho,amp_l,sig_l,xc,yc,zc,xx,yy,zz


def create_ic(field):
    if field.verb != 'silent':
        print("Creating ICs ...")
    start = time.time()

    if field.ictype == 'solitons':
        solitons_file(field)
    else:
        print("IC %s not implementet yet!"%field.ictype)
    
    '''
    Add other cases
    '''

    if field.verb != 'silent':
        print("IC took %.3f seconds\n"%(time.time()-start))



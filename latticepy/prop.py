import numpy as np
from params import DEV
if DEV == 'gpu':
    import cupy as cp


# ...........................
#   Schroedinger-Poisson
# ...........................

def PseudoKD_CPU(field):
    
    # Kick
    if field.halfstep == 1:
        field.psi    = np.exp(-1.j*0.5*field.dt*field.V)*field.psi
        field.halfstep = 0
    else:
        field.psi    = np.exp(-1.j*field.dt*field.R*field.V)*field.psi
    
    # Drift 
    psihat = np.fft.fftn(field.psi)
    pishat = np.exp(field.dt* (-1.j*0.5*field.k2))*psihat
    field.psi    = np.fft.ifftn(psihat)

    # Update
    Vhat   = -np.fft.fftn(4.0*np.pi*field.GN*(np.abs(field.psi)**2-1.0)) / ( field.k2  + (field.k2==0))
    field.V      = np.real(np.fft.ifftn(Vhat))
    updateR(field)

def PseudoKD_GPU(field):
    
    # Kick
    if field.halfstep == 1:
        field.psi_d    = cp.exp(-1.j*0.5*field.dt*field.R*field.V_d)*field.psi_d
        field.halfstep = 0
    else:
        field.psi    = cp.exp(-1.j*field.dt*field.R*field.V_d)*field.psi_d
    
    # Drift 
    psihat = cp.fft.fftn(field.psi_d)
    pishat = cp.exp(field.dt*(-1.j*0.5*field.k2_d))*psihat
    field.psi_d    = cp.fft.ifftn(psihat)

    # Update
    Vhat   = -cp.fft.fftn(4.0*cp.pi*field.GN*(np.abs(field.psi_d)**2-1.0)) / ( field.k2_d  + (field.k2_d==0))
    field.V_d      = cp.real(cp.fft.ifftn(Vhat))
    updateR(field)


def PseudoKD(field):
    if field.device == 'cpu':
        PseudoKD_CPU(field)
    elif field.device == 'cpufast':
        pass
    elif field.device == 'gpu':
        PseudoKD_GPU(field)

'''
# Old function
def PseudoKD(field):
    half = 1
    if field.device == 'cpu':
        if half == 1:
            field.psi    = np.exp(-1.j*field.dt/2.0*field.V)*field.psi
        else:
            field.psi    = np.exp(-1.j*field.dt/2.0*field.V)*field.psi
            
        # drift 
        psihat = np.fft.fftn(field.psi)
        pishat = np.exp(field.dt* (-1.j*field.k2/2.))*psihat
        field.psi    = np.fft.ifftn(psihat)
        # update potential
        Vhat   = -np.fft.fftn(4.0*np.pi*field.GN*(np.abs(field.psi)**2-1.0)) / ( field.k2  + (field.k2==0))
        field.V      = np.real(np.fft.ifftn(Vhat))
        # kick
        field.psi    = np.exp(-1.j*field.dt/2.0*field.V)*field.psi
    elif field.device == 'cpufast':
        pass
    elif field.device == 'gpu':
        # kick
        field.psi_d = cp.exp(-1.j*field.dt/2.0*field.V_d)*field.psi_d
        # drift
        psihat = cp.fft.fftn(field.psi_d)
        psihat = cp.exp(field.dt * (-1.j*field.k2_d/2.))*psihat
        field.psi_d = cp.fft.ifftn(psihat)
        # update potential
        Vhat = -cp.fft.fftn(4.0*np.pi*field.GN*(np.abs(field.psi_d)**2-1.0)) / ( field.k2_d  + (field.k2_d==0))
        field.V_d = cp.real(cp.fft.ifftn(Vhat))
        # kick
    field.psi_d = cp.exp(-1.j*field.dt/2.0*field.V_d)*field.psi_d
    # Time update
    updateR(field)
'''

# Scale factor

def updateR(field):
    if field.refR == 'MRE':
        if field.device == 'cpu':
            field.R = np.add(field.R,field.dt*field.R**3*np.sqrt(1/field.R**3+1/field.R**4))
        if field.device == 'gpu':
            field.R = cp.add(field.R,field.dt*field.R**3*cp.sqrt(1/field.R**3+1/field.R**4))
    elif field.refR == 'RD':
        pass
    elif field.refR == 'MD':
        pass
    elif field.refR == 'Static':
        field.R = 1


# Klein-Gordon (Strings)

def LeapFrog_Axion():
    return 

# Other 

# .....................................................

def propagate(field,system='SP',propa='PseudoKD'):
    if system == 'SP':
        if propa == 'PseudoKD':
            PseudoKD(field)
    elif system == 'Strings':
        #LeapFrog_Axion()
        pass
    return 

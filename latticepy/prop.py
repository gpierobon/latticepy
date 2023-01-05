import numpy as np
from params import DEV
if DEV == 'gpu':
    import cupy as cp

# Schroedinger-Poisson

def PseudoKD(field):
    if field.device == 'cpu':
        # kick
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
    

def Yoshida():
    return


# Klein-Gordon (Strings)

def LeapFrog_Axion():
    return 

# Other 

# Main call

def propagate(field,system='SP',propa='PseudoKD'):
    if system == 'SP':
        if propa == 'PseudoKD':
            PseudoKD(field)
        if propa == 'Yoshida':
            Yoshida()
    elif system == 'Strings':
        LeapFrog_Axion()
    return 


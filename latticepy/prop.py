import numpy as np
from params import DEV
if DEV == 'gpu':
    import cupy as cp


# .....................................................
#   Schroedinger-Poisson
# .....................................................

def PseudoKD(field):
    if field.device == 'cpu':
        # First 1/2 kick
        field.psi    = np.exp(-1.j*field.dt*0.5*field.V)*field.psi
        # Full drift 
        field.psihat = np.fft.fftn(field.psi)
        field.psihat = np.exp(field.dt * (-1.j*field.k2/2.))*field.psihat
        field.psi    = np.fft.ifftn(field.psihat)
        # Update
        field.updateR()
        Vhat   = -np.fft.fftn(4.0*np.pi*field.Norm*field.a*(np.abs(field.psi)**2-1.0)) / ( field.k2  + (field.k2==0))
        field.V      = np.real(np.fft.ifftn(Vhat))
        # Second 1/2 Kick
        field.psi    = np.exp(-1.j*field.dt*0.5*field.V)*field.psi
    elif field.device == 'cpufast':
        pass
    elif field.device == 'gpu':
        field.psi_d = cp.exp(-1.j*field.dt/2.0*field.V_d)*field.psi_d
        psihat = cp.fft.fftn(field.psi_d)
        psihat = cp.exp(field.dt * (-1.j*field.k2_d/2.))*psihat
        field.psi_d = cp.fft.ifftn(psihat)
        Vhat = -cp.fft.fftn(4.0*np.pi*field.Norm*(np.abs(field.psi_d)**2-1.0)) / ( field.k2_d  + (field.k2_d==0))
        field.V_d = cp.real(cp.fft.ifftn(Vhat))
        field.psi_d = cp.exp(-1.j*field.dt/2.0*field.V_d)*field.psi_d


# .....................................................
# Klein-Gordon (Axion strings) 
# .....................................................











# .....................................................

def propagate(field,system='SP',propa='PseudoKD'):
    PseudoKD(field)
    return 

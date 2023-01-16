from params import *
import numpy as np
if DEV == 'gpu':
    import cupy as cp

# Main field class 

class Field:
    def __init__(self):
        self.Ngrid=N
        self.ndims=NDIMS
        self.device=DEV
        self.boxsize=L
        self.prec=PREC
        self.verb=VERB
        self.ictype=ICTYPE
        self.icfile=ICFILE
        self.dt=dt
        self.tf=tf
        self.halfstep=1
        self.R=1
        self.refR=REFR
        self.GN=G
    
    def create_Grid(self):
        xlin = np.linspace(0,L,N+1)[0:N]
        if self.ndims == 2:
            xx,yy = np.meshgrid(xlin,xlin)
            zz = 0
        elif self.ndims == 3:
            xx,yy,zz = np.meshgrid(xlin,xlin,xlin)
        self.xx = xx
        self.yy = yy
        self.zz = zz
        if self.device == 'gpu':
            self.xx = cp.asarray(xx)
            self.yy = cp.asarray(yy)
            self.zz = cp.asarray(zz)
    
    def set_k2(self):
        klin = 2.0*np.pi/self.boxsize*np.arange(-self.Ngrid/2,self.Ngrid/2)
        if self.ndims == 2:
            kx,ky = np.meshgrid(klin,klin)
            kx = np.fft.ifftshift(kx)
            ky = np.fft.ifftshift(ky)
            self.k2 = kx**2+ky**2
            del klin,kx,ky
        elif self.ndims == 3:
            kx,ky,kz = np.meshgrid(klin,klin,klin)
            kx = np.fft.ifftshift(kx)
            ky = np.fft.ifftshift(ky)
            kz = np.fft.ifftshift(kz)
            self.k2 = kx**2+ky**2+kz**2
            del klin,kx,ky,kz
        
        if self.device == 'gpu':
            self.k2_d = cp.asarray(self.k2)

    def set_potential(self):
        if self.device == 'cpu':
            Vhat = -np.fft.fftn(4.0*np.pi*self.GN*(np.abs(self.psi)**2-1.0)) / ( self.k2  + (self.k2==0))
            self.V = np.real(np.fft.ifftn(Vhat)).astype('float32')
        elif self.device == 'gpu':
            Vhat_d = -cp.fft.fftn(4.0*np.pi*self.GN*(np.abs(self.psi_d)**2-1.0)) / ( self.k2_d + (self.k2_d==0))
            self.V_d = cp.real(cp.fft.ifftn(Vhat_d)).astype('float32')

    def copy_to_host(self):
        '''
        Implement something like this
        if system == 'sp'
        '''
        self.psi = cp.asnumpy(self.psi_d)
        self.V = cp.asnumpy(self.V_d)



         

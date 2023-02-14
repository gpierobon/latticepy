import os
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
        self.rdt=RDT
        self.tf=tf
        self.stepnum=0
        self.halfstep=1
        self.a=1.0
        self.aref=AREF
        self.Norm=NORM
        self.savedir=SAVEDIR
    
    def start_run(self):
        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        sdir = path+'/'+self.savedir
        if not os.path.exists(sdir):
            os.makedirs(sdir)
            os.makedirs(sdir+'/plots')
            os.makedirs(sdir+'/rho')
        self.sdir = sdir

    def create_Grid(self):
        xlin = np.linspace(0,self.boxsize,self.Ngrid+1)[0:self.Ngrid]
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
            Vhat = -np.fft.fftn(4.0*np.pi*self.Norm*(np.abs(self.psi)**2-1.0)) / ( self.k2  + (self.k2==0))
            self.V = np.real(np.fft.ifftn(Vhat)).astype('float32')
        elif self.device == 'gpu':
            Vhat_d = -cp.fft.fftn(4.0*np.pi*self.Norm*(np.abs(self.psi_d)**2-1.0)) / ( self.k2_d + (self.k2_d==0))
            self.V_d = cp.real(cp.fft.ifftn(Vhat_d)).astype('float32')
    
    def set_stepper(self):
        pass
        #field.dt = (field.boxsize/field.Ngrid)**2/np.pi
            
    def update_stepper(self):
        field.dt = 0.00025/field.a # Matches 2203.10100

    def set_steps(self):
        self.steps = int(np.ceil(self.tf/self.dt))
        if self.verb != 'silent':
            print("Loop will take %d steps"%self.steps)
    
    def getR(self):
        pass

    def updateR(self):
        if self.aref == 'Static':
            self.a = 1
        if self.aref == 'MRE':
            self.a *= (1+np.sqrt(1+self.a)*self.dt)


    def host_to_device(self):
        self.psi_d = cp.asarray(self.psi)


    def copy_to_host(self):
        '''
        Implement something like this
        if system == 'sp'
        '''
        self.k2  = cp.asnumpy(self.k2_d) 
        self.psi = cp.asnumpy(self.psi_d)
        self.V   = cp.asnumpy(self.V_d)



         

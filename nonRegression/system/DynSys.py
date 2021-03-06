# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:17:18 2020

@author: prith
"""

import numpy as np
import matplotlib.pyplot as plt

#x = np.random.rand(4,1)
#z = np.concatenate((x[2:],np.zeros((2,1))),axis=0)
#print(x)
#print(z)

class dynsys:
    def __init__(self,x = np.zeros((4,1)),dt=0.1,horizon=2):
        self.x = x
        self.gmat = np.array([[0, 0],
                [0, 0],
                [1, 0],
                [0, 1]])
        self.dt = dt
        self.history = np.zeros((4,horizon+1))
        self.history[:,0] = self.x[:,0]
        self.horizon = horizon
        
    
    def f(self):
        return np.concatenate((self.x[2:],np.zeros((2,1))),axis=0)
    
    def g(self,u):
        return np.dot(self.gmat,u)
    
    def update(self,u = np.zeros((2,1))):
        self.x += self.f()*self.dt + self.g(u)*self.dt
        
    def simulate(self):
        for i in range(self.horizon):
            self.update(u=np.random.rand(2,1))
            self.history[:,i+1] = self.x[:,0]

class ctrlsys:
    def __init__(self,sys = dynsys(),
                 horizon = 5,
                 params=np.zeros((dynsys().gmat.shape[1],
                                  dynsys().gmat.shape[0])),
                                  xdes = np.zeros((4,1))):
        self.system = sys
        self.params = params
        self.r = xdes
        self.horizon = horizon
        self.xhist = np.zeros((self.system.x.shape[0],horizon+1))
        self.xhist[:,0] = self.system.x[:,0]
        self.uhist = np.zeros((self.system.gmat.shape[1],horizon))
        
    
    def simulate(self):
        for i in range(self.horizon):
            error = self.r - self.system.x
            u = np.dot(self.params,error).reshape(-1,1)
            self.uhist[:,i] = u[:,0]
            self.system.update(u)
            self.xhist[:,i+1] = self.system.x[:,0]
         
        
np.set_printoptions(precision=3)
example = ctrlsys(horizon = 3, xdes = np.array([[1,1,0,0]]).transpose(),
                  params = np.array([[5,0,5,0],[0,5,0,5]]))
example.simulate()

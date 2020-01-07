# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 11:40:28 2020

@author: nickl
"""

from class_sciData import sciData
import models
import os
import matplotlib.pyplot as plt
import numpy as np
import time
start = time.time()

# %% Setting the initial Parameters
initpar = {
        'pos_L'         : -8.976e-01,
        'w_L'           :  3.300e-03 ,
        'pos_H'         : -1.677e-01,
        'w_H'           : 4.495e-02,
        'p0_H'          : -2.676e-03,
        'gammaC1'       : 2.230719e-06,
        'gammaW1'       : 5.388790e-02,
        'deltaE1'       : 3.414365e-01,
        'eta1'          : 0.78,
        'width1'        : 1.445773e-02,
        'gammaC2'       : 1.173901e-05,
        'gammaW2'       : 3.545940e-02,
        'deltaE2'       : 5.594792e-01,
        'eta2'          : 0.78,
        'width2'        : 6.554842e-03,
        'gamC_L'        : 3E-06*5.370e-03,
        'gamW_L'        : 5.370e-03+3E-06,
        'delE_L'        : 0.6,
        'eta_L'         : 5.8e-01,
        'width_L'       : 3.222e-02
        }

gamR_L = .5*(initpar['gammaW2']-np.sqrt(initpar['gammaW2']**2-4*initpar['gammaC2']))
gamR_R = initpar['gammaW2']-gamR_L
print(gamR_L)
print(gamR_R)

def memoryMolecule_gauss(vb, pos, width,p0,
                   gammaC1_H, gammaW1_H, deltaE1_H, eta1_H,sigma1_H,
                   gammaC2_H, gammaW2_H, deltaE2_H, eta2_H,sigma2_H,
                   gammaL_L, gammaR_L, deltaE_L, eta_L,width_L):
    c = 0
    vg = 0
    T = 300

    args_L = (gammaL_L, gammaR_L, deltaE_L, eta_L,width_L,c,vg,T)
    
    P_H = models.sigmoid(vb,pos,width)+(vb-1)*p0
    P_L = 1-P_H
    
    I_H = models.tunnelmodel_2level(vb,c,vg,T,
                                    gammaC1_H,gammaW1_H,deltaE1_H,eta1_H,sigma1_H,
                                    gammaC2_H,gammaW2_H,deltaE2_H,eta2_H,sigma2_H)
    I_L = models.tunnelmodel_singleLevel(vb,*args_L)
    
    return P_H*I_H+P_L*I_L

# %% Set Up The Objects
directory = '%s\\'%os.getcwd()
fNameH = 'newhighEnergy.txt'
fNameL = 'newLowEnergy.txt'
highConduct = sciData(fNameH,directory,memoryMolecule_gauss)
LowConduct = sciData(fNameL,directory,memoryMolecule_gauss,
                     scale = highConduct.scale)
xtot = np.append(highConduct.workingdat['X'],LowConduct.workingdat['X'])
yexp = np.append(highConduct.workingdat['Y'],LowConduct.workingdat['Y'])

def Everything(initpar):
    #%% Permenant
    args_H = list(initpar.values())[2:]
    mod1=highConduct.model(highConduct.workingdat['X'],*args_H)
    
    args_L = list(initpar.values())[0:2]+list(initpar.values())[5:]
    args_L.insert(2,0)
    mod2=LowConduct.model(LowConduct.workingdat['X'],*args_L)
    
    #%% Setting up the Error
    return np.append(mod1,mod2)

ythr = Everything(initpar)
residual = np.subtract(np.log(np.abs(yexp)),np.log(np.abs(ythr)))
Error = np.sqrt(np.sum(residual**2))
print('Error: %.3f'%Error)

#%% Plotting All the things
plt.figure()
plt.scatter(xtot,np.abs(yexp),s=10,color='black')
plt.plot(xtot,abs(ythr),color='red',linewidth=4)
plt.yscale('log')
plt.ylim([.00001,150])
#
#%% Time 
end = time.time()
print('Total Time (s): %d'%(end-start))
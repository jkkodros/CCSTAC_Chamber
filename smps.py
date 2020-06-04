# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 13:38:46 2020

Module for SMPS

@author: J Kodros
"""

import numpy as np
import matplotlib.pyplot as plt

class SMPS:
    def __init__(self, relTime, dp, dNdlogDp):
        self.relTime = relTime
        self.dp = dp
        self.dNdlogDp = dNdlogDp
        self.dlogDp = 1/64.
        
    def calc_dVdlogDp(self):
        # calc dVdlogDp in [nm3 cm-3]
        dVdlogDp = dNdlogDp[:,:] * np.pi/6. * (self.dp[np.newaxis,:]**3)
        self.dVdlogDp = dVdlogDp
        
    def calc_dMdlogDp(self, density=1.0):
        # calc dMdlogDp in ug m-3
        density = density * 1e-9 / (1E9**3)
        try:
            dMdlogDp = self.dVdlogDp * density
        except AttributeError:
            self.calc_dVdlogDp()
            dMdlogDp = self.dVdlogDp * density
        self.dMdlogDp = dMdlogDp
        
    def calc_Ntot(self):
        Ntot = (self.dNdlogDp * self.dlogDp).sum(axis=1)
        self.Ntot = Ntot
    
    def calc_Vtot(self):
        try:
            dVdlogDp = self.dVdlogDp
        except AttributeError:
            self.calc_dVdlogDp()
            dVdlogDp = self.dVdlogDp 
        self.Vtot = (dVdlogDp * self.dlogDp).sum(axis=1)
        
    def calc_Mtot(self):
        try:
            dMdlogDp = self.dMdlogDp
        except AttributeError:
            self.calc_dMdlogDp()
            dMdlogDp = self.dMdlogDp
        Mtot = (dMdlogDp * self.dlogDp).sum(axis=1)
        
    
        


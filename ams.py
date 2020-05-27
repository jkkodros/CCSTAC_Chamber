# -*- coding: utf-8 -*-
"""
Created on Tue May 26 13:06:37 2020

Class for AMS data

@author: J Kodros
"""

import numpy as np
import matplotlib.pyplot as plt

class AMS:
    def __init__(self, relTime, OA, NO3, SO4, NH4, Chl, AW, ON, fON, 
                 f43, f44, f60, O_C, H_C, OM_OC):
        self.relTime = relTime
        self.OA = OA
        self.NO3 = NO3
        self.SO4 = SO4
        self.NH4 = NH4
        self.Chl = Chl
        self.AW = AW
        self.ON = ON
        self.fON = fON
        self.f43 = f43
        self.f44 = f44
        self.f60 = f60
        self.O_C = O_C
        self.H_C = H_C
        self.OM_OC = OM_OC
        
    def calc_elemental_enhancements(self):
        f44_f60_ratio = self.f44/self.f60
        O_C_baseline = self.O_C[(self.relTime >= -1.0) & 
                                (self.relTime < 0.0)].mean()
        f44_f60_baseline = f44_f60_ratio[(self.relTime >= -1.0) & 
                                      (self.relTime < 0.0)].mean()
        self.O_C_enhancement = self.O_C/O_C_baseline
        self.f44_f60_ratio = f44_f60_ratio/f44_f60_baseline
        
    def calc_aerosol_enhancements(self, BC=None):
        if BC is None:
            denominator = self.SO4
        else:
            denominator = BC
        OA_ratio = self.OA/denominator
        OA_ratio_baseline = OA_ratio[(self.relTime >= -0.5) & 
                            (self.relTime < 0.0)].mean()
        self.OA_enhancement = OA_ratio / OA_ratio_baseline
        NO3_ratio = self.NO3/denominator
        NO3_ratio_baseline = NO3_ratio[(self.relTime >= -0.5) & 
                            (self.relTime < 0.0)].mean()
        self.NO3_enhancement = NO3_ratio / NO3_ratio_baseline
        
    def calc_total_mass(self, DRY=True):
        total_mass = self.OA + self.NO3 + self.SO4 + self.NH4 + self.Chl 
        if not DRY:
            total_mass += self.AW
        return total_mass
        
    #def triangle_plots(self):
    #    fig, ax = plt.subplots(2)
    #    ax.plot(sallyX, rightRed, color='red', linestyle='dashed', linewidth=1.5, zorder=-1)
    #    ax1.plot(sallyX, leftBlue, color='blue', linestyle='dashed', linewidth=1.5, zorder=-1)
    #    sc1 = ax1.scatter(f43_exp14, f44_exp14, marker='o', s=100, facecolors='none'\
    #              , c=relTime_exp14, cmap='autumn_r')
            
    def plot_aerosol_timeseries(self):
        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(self.relTime, self.OA, linewidth=2, color='green')
        ax.set_ylabel('OA [$\mu$g $^{-3}$]')
        ax.set_ylim(0)
        ax2 = ax.twinx()
        ax2.plot(self.relTime, self.NO3, linewidth=2, color='blue')
        ax2.plot(self.relTime, self.SO4, linewidth=2, color='red')
        ax2.plot(self.relTime, self.NH4, linewidth=2, color='orange')
        ax2.plot(self.relTime, self.Chl, linewidth=2, color='purple')
        ax2.set_ylabel('non-OA [$\mu$g m$^{-3}$]')
        ax2.set_ylim(0.)
        ax.set_xlim(-4, 6)
        plt.show()


# -*- coding: utf-8 -*-
"""
Created on Tue May 26 13:06:37 2020

Class for AMS data

@author: J Kodros
"""

import numpy as np
import matplotlib.pyplot as plt

from CCSTAC_Chamber import chamber_func_tools as chamber_tools

class AMS:
    def __init__(self, relTime, OA, NO3, SO4, NH4, Chl, AW, ON, fON, 
                 f43, f44, f60, O_C, H_C, OM_OC):
        self.relTime = relTime
        self.OA = OA
        self.NO3 = NO3
        self.IN = NO3 - ON
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
        
    def calc_enhancement_ratio(self, series, base_time=[-0.5, 0]):
        series_baseline = series[(self.relTime > base_time[0]) &
                                 (self.relTime <= base_time[1])].mean()
        enhancement_ratio = series/series_baseline
        return enhancement_ratio
        
    def calc_elemental_enhancements(self):
        self.O_C_enhancement = self.calc_enhancement_ratio(self.O_C)
        self.f44_f60_enhancement = self.calc_enhancement_ratio(
            self.f44/self.f60)
        
    def calc_elemental_deltas(self):
        self.delta_O_C = self.O_C - self.O_C[(self.relTime > -0.5) & 
                                            (self.relTime < 0.0)].mean()
        f44_f60 = self.f44/self.f60
        self.delta_f44_f60 = f44_f60 - f44_f60[(self.relTime > -0.5) & 
                                            (self.relTime < 0.0)].mean()
        
        
    def calc_aerosol_enhancements(self, BC=None):
        if BC is None:
            denominator = self.SO4
        else:
            denominator = BC
        species = [self.OA, self.NO3, self.IN, self.ON]
        ratios = [spec/denominator for spec in species]
        ERS = [*map(self.calc_enhancement_ratio, ratios)]
        self.OA_enhancement = ERS[0]
        self.NO3_enhancement = ERS[1]
        self.IN_enhancement = ERS[2]
        self.ON_enhancement = ERS[3]

    def calc_total_mass(self, DRY=True):
        total_mass = self.OA + self.NO3 + self.SO4 + self.NH4 + self.Chl 
        if not DRY:
            total_mass += self.AW
        return total_mass
        
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
        #plt.show()
        return fig, ax
    
    def triangle_plots(self, startTime=-1, endTime=3):
        index_bol = (self.relTime >= startTime) & (self.relTime <= endTime)
        fig, ax = plt.subplots(1, 2, figsize=(12,6))
        ax[0].scatter(self.f43[index_bol], self.f44[index_bol], 
                      c=self.relTime[index_bol], cmap='jet')
        x_line = [0.02, 1.02]
        right_red = [0.295024, -1.54878]
        left_blue = [0.294992, -5.72541]
        ax[0].set_xlim(0, 0.3)
        ax[0].set_ylim(0, 0.3)
        ax[0].set_xlabel('f$_{43}$')
        ax[0].set_ylabel('f$_{44}$')
        #cbar = ax[0].colorbar()
        plt.show()


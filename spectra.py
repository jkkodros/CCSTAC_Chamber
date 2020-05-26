# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:49:30 2020

Class for AMS spectra (maybe spectra generally)?

@author: J Kodros
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

class Spectra:
    def __init__(self, mz, data, relTime=None):
        self.mz = mz
        self.data = data
        self.relTime = relTime
        
    def convert_to_umr(self):
        if type(self.relTime) == np.ndarray:
            timeSeries = True
        else:
            timeSeries = False
        self.mz_umr = np.arange(12, int(max(self.mz))+1, 1)
        if timeSeries:
            self.data_umr = np.zeros((len(self.data),len(self.mz_umr)))
        else:
            self.data_umr = np.zeros(len(self.mz_umr))
    
        for i in range(0, len(self.mz_umr)):
            ix1 = np.where(self.mz >= self.mz_umr[i] - 0.5 )[0][0]
            ix2 = np.where(self.mz < self.mz_umr[i] + 0.5)[0][-1]
            if timeSeries:
                self.data_umr[:,i] = self.data[:,ix1:ix2+1].sum(1)
            else:
                self.data_umr[i] = self.data[ix1:ix2+1].sum()
                
    def normalize_spectra(self):
        if type(self.relTime) == np.ndarray:
            self.data_umr_normalized = np.zeros(np.shape(self.data_umr))
            for i in range(0, len(self.data_umr)):
                self.data_umr_normalized[i,:] = (self.data_umr[i,:]
                                                 /self.data_umr[i,:].sum())

    def plot_spectra(self, time_period=[[-0.5, 0.0]], UMR=True, 
                     normalized=True):
        if type(self.relTime) == np.ndarray:
            spectras = []
            for period in time_period:
                spectra = self.data_umr[(self.relTime >= period[0]) & (
                    self.relTime < period[1]), :].mean(axis=0)
                if normalized:
                    spectra = spectra / spectra.sum()
                spectras.append(spectra)
        else:
            spectra = self.data_umr
            
        fig, ax = plt.subplots(figsize=(10,5))
        if len(spectra) > 1:
            ax.bar(self.mz_umr, spectras[0], color='C2')
            ax.plot(self.mz_umr, spectras[1], 'o', color='k')
        ax.set_xlabel('m/z', fontsize=14)
        ax.set_ylabel('Normalized Spectra', fontsize=14)
        ax.set_ylim(0.0)
        ax.set_xlim(12, 100)
        ax.set_xticks([20, 30, 40, 50, 60, 70, 80, 90, 100])
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.grid(which='major', axis='x', color='grey', linestyle='dashed', alpha=0.6)
        fig.tight_layout()
        return fig, ax
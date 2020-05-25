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
    def __init__(self, mz, data):
        self.mz = mz
        self.data = data
        
    def convert_to_umr(self):
        if len(self.data) > 1:
            timeSeries = True
        else:
            timeSeries = False
        self.mz_umr = np.arange(12, int(max(self.mz))+1, 1)
        if timeSeries:
            self.data_umr = np.zeros((len(self.data),len(self.mz)))
        else:
            self.data_umr = np.zeros(len(self.mz))
    
        for i in range(0, len(self.mz_umr)):
            ix1 = np.where(self.mz >= self.mz_umr[i] - 0.5 )[0][0]
            ix2 = np.where(self.mz < self.mz_umr[i] + 0.5)[0][-1]
            if timeSeries:
                self.data_umr[:,i] = self.data[:,ix1:ix2+1].sum(1)
            else:
                self.data_umr[i] = self.data[ix1:ix2+1].sum()

    def plot_spectra(self, time_period, UMR=True, spectra2=None):
        if len(self.data_umr) > 1:
            spectra = self.data_umr.mean(axis=0)
        else:
            spectra = self.data_umr
            
        fig, ax = plt.subplots(figsize=(10,5))
        ax.bar(self.mz, spectra, color='C2')
        if spectra2:
            ax.plot(spectra2.mz, spectra2.data, 'o', color='k')
        
        ax.set_xlabel('m/z', fontsize=14)
        ax.set_ylabel('Normalized Spectra', fontsize=14)
        ax.set_ylim(0.0)
        ax.set_xlim(12, 100)
        ax.set_xticks([20, 30, 40, 50, 60, 70, 80, 90, 100])
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.grid(which='major', axis='x', color='grey', linestyle='dashed', alpha=0.6)
        fig.tight_layout()
        return fig, ax
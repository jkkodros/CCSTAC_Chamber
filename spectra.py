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
        self.data_umr = self.convert_to_umr()
        self.data_umr_normalized = self.normalize_spectra()
        
    def convert_to_umr(self):
        self.mz_umr = np.arange(12, int(max(self.mz))+1, 1)
        data_umr = np.zeros(len(self.mz_umr))
        for i in range(0, len(self.mz_umr)):
            ix1 = np.where(self.mz >= self.mz_umr[i] - 0.5 )[0][0]
            ix2 = np.where(self.mz < self.mz_umr[i] + 0.5)[0][-1]
            data_umr[i] = self.data[ix1:ix2+1].sum()
        return data_umr
                
    def normalize_spectra(self):
        data_umr_normalized = (self.data_umr/self.data_umr.sum())
        return data_umr_normalized
    
    def calc_theta_angle(self, spectra2):
        dot_product = np.dot(self.data_umr, spectra2.data_umr)
        len1 = (np.dot(self.data_umr, self.data_umr))**(0.5)
        len2 = (np.dot(spectra2.data_umr, spectra2.data_umr))**(0.5)
        theta_angle = np.arccos(dot_product/(len1*len2)) * 180./np.pi
        return theta_angle

    def plot_spectra(self, spectra2=None, UMR=True, normalized=True):
        fig, ax = plt.subplots(figsize=(10,5))
        ax.bar(self.mz_umr, self.data_umr, color='C2')
        if spectra2:
            ax.plot(spectra2.mz_umr, spectra2.data_umr, 'o', color='k')
        ax.set_xlabel('m/z', fontsize=14)
        ax.set_ylabel('Normalized Spectra', fontsize=14)
        ax.set_ylim(0.0)
        ax.set_xlim(12, 100)
        ax.set_xticks([20, 30, 40, 50, 60, 70, 80, 90, 100])
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.grid(which='major', axis='x', color='grey', linestyle='dashed', alpha=0.6)
        fig.tight_layout()
        return fig, ax
    
class SpectraMatrix(Spectra):
    def __init__(self, mz, data, relTime):
        #super().__init__(mz, data)
        self.mz = mz
        self.data = data
        self.relTime = relTime
        self.data_umr = []
        self.data_umr_normalized = []
            
        
    def convert_to_umr(self):
        pass
            
    
    def normalize_spectra(self):
        pass
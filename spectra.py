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
import time

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
    
class SpectraMatrix:
    def __init__(self, mz, data, relTime):
        #super().__init__(mz, data)
        self.mz = mz
        self.data = data
        self.relTime = relTime
        
    def timer(func):
        def wrapper(*args, **kwargs):
            t_start = time.time()
            result = func(*args, **kwargs)
            t_total = time.time() - t_start
            print('{} took {} seconds to run'.format(func.__name__, t_total))
            return result
        return wrapper

    #@timer
    def convert_to_umr(self):
        df = pd.DataFrame(data=self.data, columns=self.mz)
        df = df.transpose().reset_index()
        df = df.rename(columns={'index': 'mz'})
        df['mz'] = df['mz'].round()
        df_grouped = df.groupby('mz')
        df_umr = df_grouped.sum().transpose()
        self.data_umr = df_umr.values
        self.mz_umr = df_umr.columns.values
        return self.mz_umr, self.data_umr
    
    #@timer
    def normalize_spectra(self, UMR=True):
        if UMR:
            data = self.data_umr
        else:
            data = self.data
        total = data.sum(axis=1)
        self.data_normalized = data[:,:] / total[:,np.newaxis]
        return self.data_normalized
    
    def get_mz(self, mz, UMR=True, NORM=False):
        if UMR:
            data = self.data_umr
            mz_s = self.mz_umr           
        else:
            data = self.data
            mz_s = self.mz
        data_at_mz = data[:, mz_s==mz].flatten()
        if NORM:
            data_at_mz = data_at_mz / data.sum(axis=1)
        return data_at_mz
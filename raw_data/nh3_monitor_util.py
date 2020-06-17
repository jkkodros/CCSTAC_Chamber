# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:56:00 2020

@author: J Kodros
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir


from CCSTAC_Chamber.raw_data import raw_data_util


class NH3(raw_data_util.RawDataFile):
    '''Class for processing raw nh3 monitor data files'''
    
    def __init__(self, directory, zero=-0.8, window=5):
        self.directory = directory
        self.files = listdir(directory)
        self.zero = zero
        self.window = window
        
    def _read_files(self, file):
        df = pd.read_csv(self.directory + file, encoding='latin1', 
                         skiprows=1, delimiter=';')
        df['dateTimes'] = pd.to_datetime((df['DateTime'] - 25569) * 
                                         86400.0, unit='s')
        df['dateTimes'] = df['dateTimes'].dt.round('min')
        df = df[['dateTimes', 'NH3 [ppb]']]
        df.rename(columns={'NH3 [ppb]': 'NH3_raw'}, inplace=True)
        return df
    
    def _subtract_offset(self):
        self.data['NH3_raw'] -= self.zero
        
    def _rolling_mean(self):
        self.data['NH3_ppb'] = self.data['NH3_raw'].rolling(self.window).mean()
        
    def load_data(self):
        frames = [*map(self._read_files, self.files)]
        data = pd.concat(frames) 
        self.data = data
        self._subtract_offset()
        self._rolling_mean()
        
    def plot_nh3(self, plot_raw=False, tval='dateTimes', tspan=None):
        fig, ax = plt.subplots(figsize=(12, 6))
        if plot_raw:
            ax.plot(self.data[[tval]], self.data[['NH3_raw']], 
                    color='red')
        ax.plot(self.data[[tval]], self.data[['NH3_ppb']], color='blue')
        if tspan:
            ax.set_xlim(tspan[0], tspan[1])
        elif tval=='relTime':
            ax.set_xlim(-1, 3)
        ax.set_ylim(-1.0)
        ax.set_xlabel('Time [hr]')
        ax.set_ylabel('NH$_{3}$ ppb')
        fig.tight_layout()
        return fig, ax
    

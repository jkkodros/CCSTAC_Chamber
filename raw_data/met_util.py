# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 15:54:18 2020

Package for reading in raw met files (T/RH sensor)

@author: J Kodros
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from CCSTAC_Chamber.raw_data import raw_data_util

class MetSensor(raw_data_util.RawDataFile):
    '''Class to read and process raw met files for CSTACC chamber experiments
    '''
    
    def __init__(self, directory, filename):
        super().__init__(directory, filename)

    def load_data(self):
        data = pd.read_csv(self.directory + self.filename, 
                           skiprows=7, delim_whitespace=True)
        data['dateTimes'] = pd.to_datetime(data['LogDate'] + ' '
                                           + data['LogTime'])
        data.rename(columns={'1-P': 'RH', 
                            '%RH': 'T'}, inplace=True)
        to_drop = ['LogDate', 'LogTime', '1-A', '°C', 'DataPoint']
        data.drop(to_drop, axis=1, inplace=True)
        self.data = data
        
    def plot_met(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(self.data[['relTime']], self.data[['T']], 
                color='k', linewidth=2)
        ax2 = ax.twinx()
        ax2.plot(self.data[['relTime']], self.data[['RH']], 
                 color='red', linewidth=2)
        ax.set_xlabel('Time [hr]')
        ax.set_ylabel('Temperature [C]')
        ax2.set_ylabel('RH [%]', color='red')
        ax.set_ylim(0, 30)
        ax2.set_ylim(0)
        ax.set_xlim(-1, 6)
        fig.tight_layout()
        return fig, ax
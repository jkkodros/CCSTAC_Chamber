# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:04:58 2020

Package for reading in raw Monitor data

@author: LAQS
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class MonitorsLabview:
    '''Class to process raw gas monitor data from lab from the labview
     '''

    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename
        self.offsets = {'NH3_ppb': 0.387}
    
    def load_data(self):
        data = pd.read_csv(self.directory + self.filename, 
                           delim_whitespace=True)
        data.reset_index(inplace=True)
        data['dateTimes'] = pd.to_datetime(data['level_0'] + ' '
                                           + data['level_1'])
        to_drop = ['level_0', 'level_1', 'DateTime_US', 
                   'DateTime_EU', 'SO2_ppb']
        data.drop(to_drop, axis=1, inplace=True)
        self.data = data

    def subtract_offsets(self, offsets=None):
        for col in list(self.data.columns):
            offset = self.offsets.get(col)
            if offset:
                self.data[col] -= offset

    def plot_time_series(self, tspan=None):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(self.data[['dateTimes']], self.data[['NO2_ppb']], color='k')
        ax.plot(self.data[['dateTimes']], self.data[['O3_ppb']], color='red')
        if tspan:
            ax.set_xlim(tspan[0], tspan[1])
        ax.set_xlabel('Date and Time')
        ax.set_ylabel('ppb')
        fig.tight_layout()
        return fig, ax
    
    def set_relative_time(self, zero_time):
        self.data['relTime'] = (self.data['dateTimes']
                                - zero_time).dt.total_seconds()/3600.
        
    def write_out(self, outname):
        self.data.to_csv(outname, index=False)

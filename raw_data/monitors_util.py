# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:04:58 2020

Package for reading in raw Monitor data

@author: LAQS
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from CCSTAC_Chamber.raw_data import raw_data_util


class MonitorsLabview(raw_data_util.RawDataFile):
    '''Class to process raw gas monitor data from lab from the labview
     '''

    def __init__(self, directory, filename):
        super().__init__(directory, filename)
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

    def plot_time_series(self, tspan=None, species=['NO2', 'O3'], 
                         tval='dateTimes'):
        colors = {'NO2_ppb': 'k',
                  'O3_ppb': 'red',
                  'NO_ppb': 'green',
                  'NH3_ppb': 'blue',
                  'CO2_ppb': 'purple',
                  'CO_ppb': 'k'}
        fig, ax = plt.subplots(figsize=(12, 6))
        for spec in species:
            # In case user inputs 'NO2' instead of 'NO2_ppb'
            val = spec.split('_')[0] + '_ppb'
            ax.plot(self.data[tval], self.data[[val]], 
                    color=colors.get(val))
        if tspan:
            ax.set_xlim(tspan[0], tspan[1])
        ax.set_xlabel('Time')
        ax.set_ylabel('ppb')
        fig.tight_layout()
        return fig, ax


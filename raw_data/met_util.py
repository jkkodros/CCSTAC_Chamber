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
        
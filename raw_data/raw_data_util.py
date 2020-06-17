# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:27:43 2020

Abstract class for processing raw data files from the chamber instruments

@author: J Kodros
"""

import numpy as np
import pandas as pd


class RawDataFile:
    '''Parent class for processing the raw data files from the CSTAC
    lab instruments'''

    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename
        
    def set_relative_time(self, zero_time):
        try:
            self.data['relTime'] = (self.data['dateTimes']
                                    - zero_time).dt.total_seconds()/3600.
        except AttributeError:
            print('Data not yet loaded. Load data first.')

    def write_out(self, outname):
        try:
            self.data.to_csv(outname, index=False)
        except AttributeError:
            print('No dataset loaded.')
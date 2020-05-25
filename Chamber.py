# -*- coding: utf-8 -*-
"""
J Kodros

Class and methods for analysis and plotting of CCSTAC/FORTH BB Chamber
experiments.
"""

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#%%
# =============================================================================
# BB experiment class
# =============================================================================
class Experiment:
    def __init__(self, experiment_name):
        self.experiment_name = name
        
    def load_data(dataset='Main', nitrogen_peaks=False):
        if nitrogen_peaks:
            directory = ('C:/Users/LAQS/Documents/FORTH/projects/'
                         + 'darkChemistry/uniform_series_analysis/'
                         + 'experiments_nContainingPeaks/')
        else:
            directory = ('C:/Users/LAQS/Documents/FORTH/projects/'
                         + 'darkChemistry/uniform_series_analysis/'
                         + 'experiments/')
            
        if dataset == 'Main':
            filename = self.experiment_name + '_mainTimeSeries_uniform.csv'
            data = pd.read_csv(directory + filename)
            self.OA = data['OA'].values
        elif dataset == 'PTRMS':
            filename = self.experiment_name + '_VOC_uniform.csv'
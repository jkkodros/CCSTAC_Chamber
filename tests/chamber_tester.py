# -*- coding: utf-8 -*-
"""
Created on Mon May 25 14:06:48 2020

Tester routine for dark BB Chamber experiment class

@author: J Kodros
"""

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from CCSTAC_Chamber import chamber 

#%%
# =============================================================================
# Plotting variables
# =============================================================================
plt.close('all')
plt.rc('font', family='serif')
plt.rc('font', size=14)


#%%
# =============================================================================
# Create Experiment object
# =============================================================================
experiment = chamber.Experiment('Exp14')
print(experiment)

#%%
# =============================================================================
# Load data
# =============================================================================
#data = experiment.get_dataset()

experiment.load_data(['AMS', 'MAAP', 'Monitors', 'SMPS', 'Met'])

fig = plt.figure()
plt.plot(experiment.relTime, experiment.OA, color='green')
plt.plot(experiment.relTime, experiment.NO3, color='blue')
plt.show()

fig = plt.figure()
plt.plot(experiment.relTime, experiment.O3)
plt.plot(experiment.relTime, experiment.NO2)

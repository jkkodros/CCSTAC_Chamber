# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:58:28 2020

Test script for default analysis plots

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
# Instantiate experiment and load data
# =============================================================================
experiment = chamber.Experiment('Exp14')

#%%
# =============================================================================
# Load data 
# =============================================================================
experiment.load_data(['AMS', 'SMPS'])

#%%
# =============================================================================
# Default AMS species plot
# =============================================================================
fig, ax = experiment.ams.plot_aerosol_timeseries()

#%%
# =============================================================================
# Plot SMPS N, V, M
# =============================================================================
experiment.smps.calc_Ntot()


fig, ax = plt.subplots(figsize=(12,6))
plt.plot(experiment.relTime, experiment.smps.Ntot)
#plt.plot(experiment.relTime, N)
plt.show()
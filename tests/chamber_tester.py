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

experiment.load_data(['AMS', 'Mass Balance Factors'])

#%%
# =============================================================================
# Plot AMS properties
# =============================================================================
experiment.ams.plot_aerosol_timeseries()
experiment.ams.calc_elemental_enhancements()
experiment.ams.calc_aerosol_enhancements()

plt.figure()
plt.plot(experiment.relTime, experiment.ams.O_C_enhancement)
plt.plot(experiment.relTime, experiment.ams.OA_enhancement)
plt.plot(experiment.relTime, experiment.ams.NO3_enhancement)
plt.xlim(-1, 3)
plt.ylim(0.9, 5)
plt.show()

#%%
# =============================================================================
# Plot MB spectra, time series
# =============================================================================
experiment.initial_spectra.plot_spectra(spectra2=experiment.produced_spectra)

theta_angle = experiment.initial_spectra.calc_theta_angle(
    experiment.produced_spectra)

fig = plt.figure()
plt.plot(experiment.relTime, experiment.produced_OA)
plt.plot(experiment.relTime, experiment.initial_OA, color='green')
plt.ylim(0, 55)
plt.xlim(-1, 3)
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:34:15 2020

Spectra tester

@author: J Kodros
"""

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from CCSTAC_Chamber import chamber 

#%%
# =============================================================================
# Read in experiment
# =============================================================================
exp = chamber.Experiment('Exp14')

#%%
# =============================================================================
# Load data
# =============================================================================
exp.load_data(['OA_Spectra'])

#%%
# =============================================================================
# Convert to UMR
# =============================================================================
mz_umr, data_umr = exp.spectra.convert_to_umr()

# test if the values are what we expect
org44 = data_umr[:, mz_umr==44]

indices_44 = (exp.spectra.mz >= 43.5) & (exp.spectra.mz < 44.5)
org44_hr = exp.spectra.data[:, indices_44].sum(axis=1)

plt.figure()
plt.plot(exp.relTime, org44)
plt.plot(exp.relTime, org44_hr)

#%%
# =============================================================================
# Normalize
# =============================================================================
data_norm = exp.spectra.normalize_spectra()

f44 = data_norm[:, exp.spectra.mz_umr==44]

exp.load_data(['AMS'])
f44_ams = exp.ams.f44

plt.figure()
plt.plot(exp.relTime, f44)
plt.plot(exp.relTime, f44_ams)
plt.xlim(-3, 4)
plt.ylim(0, 0.1)

#%%
# =============================================================================
# Get value
# =============================================================================
org44 = exp.spectra.get_mz(44.0, NORM=True)
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
from scipy import optimize


from CCSTAC_Chamber import spectra
from CCSTAC_Chamber import ams
from CCSTAC_Chamber import smps
from CCSTAC_Chamber import chamber_func_tools as chamber_tools

#%%
# =============================================================================
# BB experiment class
# =============================================================================
class Experiment:
    def __init__(self, experiment_name, nitrogen_peaks=False):
        self.experiment_name = experiment_name
        if nitrogen_peaks:
            self.data_directory = ('C:/Users/LAQS/Documents/FORTH/projects/'
                         + 'darkChemistry/uniform_series_analysis/'
                         + 'experiments_nContainingPeaks/')
        else:
            self.data_directory = ('C:/Users/LAQS/Documents/FORTH/projects/'
                         + 'darkChemistry/uniform_series_analysis/'
                         + 'experiments/'+self.experiment_name+'/')
        
    def __repr__(self):
        return 'Experiment: {exp_name}'.format(exp_name=self.experiment_name)
    
    def get_dataset(self):
        # Return the master dataset as a pandas data frame
        filename = self.experiment_name + '_master_dataset.csv'
        data = pd.read_csv(self.data_directory + filename, header=[0,1])
        data = data.mask(data == -999)
        return data
    
    def get_mass_balance_time_series_dataset(self):
        suffix = '_massBalanceFactorizationUniform_timeseries.csv'
        filename = self.experiment_name + suffix
        df = pd.read_csv(self.data_directory + filename)
        return df
    
    def get_mass_balance_spectra_dataset(self):
        filename = self.experiment_name + ('_massBalanceFactorizationUniform'
                                           + '_spectra.csv')
        df = pd.read_csv(self.data_directory + filename)
        return df
        
    def load_data(self, datasets=['AMS']):            
        filename = self.experiment_name + '_master_dataset.csv'
        data = self.get_dataset()
        self.relTime = data[('Time', 'relTime')].values
        
        for dataset in datasets:
            try:
                if dataset == 'AMS':                    
                    OA = data[(dataset, 'HROrg')].values
                    NO3 = data[(dataset, 'HRNO3')].values
                    SO4 = data[(dataset, 'HRSO4')].values
                    NH4 = data[(dataset, 'HRNH4')].values
                    Chl = data[(dataset, 'HRChl')].values
                    AW = data[(dataset, 'HRAW')].values
                    ON = data[(dataset, 'ON')].values
                    fON = data[(dataset, 'fON')].values
                    f43 = data[(dataset, 'f43')].values
                    f44 = data[(dataset, 'f44')].values
                    f60 = data[(dataset, 'f60')].values
                    O_C = data[(dataset, 'O_C')].values
                    H_C = data[(dataset, 'H_C')].values
                    OM_OC = data[(dataset, 'OM_OC')].values
                    self.ams = ams.AMS(self.relTime, OA, NO3, SO4, NH4, Chl,
                                       AW, ON, fON, f43, f44, f60, 
                                       O_C, H_C, OM_OC)
                elif dataset == 'MAAP':
                    self.BC = data[(dataset, 'BC')].values
                elif dataset == 'Monitors':
                    self.NO = data[(dataset, 'NO')].values
                    self.NO2 = data[(dataset, 'NO2')].values
                    self.O3 = data[(dataset, 'O3')].values
                    self.NH3 = data[(dataset, 'NH3')].values
                elif dataset == 'SMPS':
                    #self.Ntot = data[(dataset, 'Ntot')].values
                    #self.Vtot = data[(dataset, 'Vtot')].values
                    #self.Mtot = data[(dataset, 'Mtot')].values
                    df_dNdlogDp = data[('SMPS_N')]
                    dp = [*map(float, list(df_dNdlogDp.columns))]
                    dNdlogDp = df_dNdlogDp.values
                    self.smps = smps.SMPS(self.relTime, dp, dNdlogDp)
                elif dataset == 'Met':
                    self.temperature = data[(dataset, 'T')].values
                    self.RH = data[(dataset, 'RH')]
                elif dataset == 'OA_Spectra':
                    df_spectra = data[(dataset)]
                    data_ms = df_spectra.values
                    mz = df_spectra.columns[:].values.astype('float')
                    self.spectra = spectra.Spectra(mz, data_ms, 
                                                   relTime=self.relTime)
                elif dataset == 'Mass Balance Factors':
                    df_timeseries = self.get_mass_balance_time_series_dataset()
                    self.initial_OA = df_timeseries['OA_initial'].values
                    self.produced_OA = df_timeseries['OA_produced'].values
                    
                    df_spectra = self.get_mass_balance_spectra_dataset()
                    mz = df_spectra['AMU'].values
                    initial_data = df_spectra['InitialFasma'].values
                    produced_data = df_spectra['ProducedFasma'].values
                    self.initial_spectra = spectra.Spectra(mz, initial_data)
                    self.produced_spectra = spectra.Spectra(mz, produced_data)
                
            except KeyError:
                print('Subset "{dataset}" not found in master dataset.'.format(
                    dataset=dataset), ' Check file or spelling')
                
    def calc_PM1(self, AMS=True):
        try:
            if AMS:
                PM1 = self.ams.calc_total_mass() 
                PM1 += self.BC
            else:
                PM1 = self.Mtot
            self.PM1 = PM1
        except AttributeError:
            print('Data not yet loaded. Load AMS+MAAP or SMPS first')
            
    def fit_wall_loss_rate(self, series=None, fitTimes=[-1.75, -1.5, 0.0],
                           k_initial = 0.042):
        # If series is none use measured wall lass rate
        if series is None:
            kwall = k_initial
            self.kwall = kwall
        
        # Or fit to series (usually BC or SO4)
        else:
            y0 = series[(self.relTime >= fitTimes[0]) & 
                        (self.relTime <= fitTimes[1])].mean()
            yFit = series[(self.relTime >= fitTimes[0]) & 
                          (self.relTime <= fitTimes[2])]
            xFit = self.relTime[(self.relTime >= fitTimes[0]) & 
                           (self.relTime <= fitTimes[2])] 
            d = self.relTime[np.abs(self.relTime - fitTimes[0]).argmin()]
        
            # Optimized curve fitting
            popt, popv = optimize.curve_fit(
                lambda x, c: chamber_tools.first_order_loss_func(x, y0, c, d), 
                xFit, yFit, p0=k_initial)
            self.kwall = popt
        
    def mass_balance_series(self, series, initial_times=[-1.75, -1.5]):
        # Get initial parameters
        y0 = series[(self.relTime >= initial_times[0]) &
                (self.relTime <= initial_times[1])].mean()
        d = self.relTime[np.abs(self.relTime - initial_times[0]).argmin()]
    
        # Fresh OA decays only from wall loss
        try:
            series_initial = chamber_tools.first_order_loss_func(
                self.relTime, y0, self.kwall, d)
        except AttributeError:
            print('kwall not yet defined. Call fit_wall_loss_rate first.')
     
        # Produced OA
        series_produced = series - series_initial
        
        return series_initial, series_produced

    def calc_produced_aerosol(self, initial_times=[-1.75, -1.5]):
        species = [self.PM1, self.ams.OA, self.ams.NO3, self.ams.SO4, 
                   self.ams.NH4, self.ams.Chl]
        initial_all = []
        produced_all= []
        for spec in species:
            initial, produced = self.mass_balance_series(spec, initial_times)
            initial_all.append(initial)
            produced_all.append(produced)
            
        self.PM_initial = initial_all[0]
        self.OA_initial = initial_all[1]
        self.NO3_initial = initial_all[2]
        self.SO4_initial = initial_all[3]
        self.NH4_initial = initial_all[4]
        self.Chl_initial = initial_all[5]
            
        self.PM_produced = produced_all[0]
        self.OA_produced = produced_all[1]
        self.NO3_produced = produced_all[2]
        self.SO4_produced = produced_all[3]
        self.NH4_produced = produced_all[4]
        self.Chl_produced = produced_all[5]
        
        
# -*- coding: utf-8 -*-
"""
This scripts converts and plots frequency spectra
from dBm to A^2/Hz or V^2/Hz

Created on Mon Dec  7 18:31:13 2020

@author: Stinky
"""
import numpy as np
import matlplotlib.pyplot as plt
import os

#define final unit to plot
unit = 'volts' # volts2, amps2, volts, amps.


# path = 'D:\\Users\\Stinky\\Google Drive\\ITA\\Data\\6 - Noise Analysis'
filename = '10hz-10khz_1kHz_1V_funcgen.dat'

# read frequency spectrum in dBm
def import_spec(filename):
    
    # Separating data from header automatically
    all_data = pd.read_csv(filename, sep = ';',header=None)
    # Type, FSL-3, 
    header_size = all_data[0] == 'Values' # last header item
    header_size = np.where(header_size)[0] # array with positions of true
    header_size = header_size[0] # converting first value to integer value
    
    data = pd.read_csv(filename, sep = ';', header = header_size)
    header = pd.read_csv(filename, sep = ';', header=None, nrows=header_size+1)
    
    data.columns = ['freq','dbm','units']
    
    #------- Power spectrum density
    # the key here is to normalize the RBW to 1 Hz
    # S = P_dbm - 10*log(RBW / 1 Hz) 
        
    #getting RBW automatically
    ind = header[0]=='RBW'    # boolean state vector to find RBW
    RBW = header[1].loc[ind]    # taking value in the second column
    RBW = RBW.reset_index(drop=True) # resenting index to start from 0 again
    RBW = float(RBW[0]) # converting string value to float
        
    S = data.dbm - 10*np.log10(RBW) #dbm/Hz
    return S

def dbm2amps2(S):
    amps2 = (10**(0.1*S) )/50
    return amps2

def amps2_2_amps(amps2):
    amps = np.sqrt(amps2)
    return amps
        
def dbm2volts2(S):
    volts2 = (10**(0.1*S) )*50
    return volts2

def volts2_2_volts(volts2):
    volts = np.sqrt(volts2)
    return volts
    
#code main loop
S = import_spec(filename)

if unit == 'volts2':
    volts2 = dbm2volts2(S)
elif unit == 'amps2':
    amps2 = dbm2amps2(S)
elif unit == 'amps':
    amps2 = dbm2amps2(S)
elif unit == 'volts':
    amps2 = dbm2amps2(S)
    
    
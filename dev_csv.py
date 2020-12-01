# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 18:43:13 2020

@author: Stinky

Test: Create .CSV files to store waveform data from oscilloscope

2 types of file:

--- 1st type: one single file with all the previous important data organized    
    accordingly with matlab script to calculate the response frequency and 
    plot it:
    Vmax, Vmin, Phase, Vin, Freq, Error, THD, Vsignal_max, Vsignal_min                   

--- 2nd type: multiple csv files, each one will correspond to one line of 1st
    file. Containing the entire waveform.

The default size for the manually collected data is 58 KB with 4 columns
    t, v1, v2, v3


"""

import pandas as pd

# I chose to use pandas to handle csv files instead of the default csv library
# because of the probability to handle with head modifications and other calculations

# importation
path = 'csv files/'
data = pd.read_csv(path + 'print_00.csv') # data frame

# exportation
waveform = data #pretending it is a brand new data acquired by oscilloscope
# waveform = pd.DataFrame() #maybe I would have to convert it to a data frame
waveform.to_csv(path + 'waveform.csv') #because it alread is a DataFrame

##########################################
# 1st Type:
# To append new line to csv: Every iteration must have the next line with the
# # actual values for that measurement
# Vmax = 
# Vmin = 

# oscilloscope.write(':MEASure:PHASe?\sCHANnel1,CHANnel2')
# sleep(0.05) # 50 ms
# Phase = oscilloscope.read(512)

# calculated_values = \
#     [Vmax, Vmin, Phase, Vin, Freq, Error, THD, Vsignal_max, Vsignal_min]
# calculated_values.to_csv('1st_type.csv', mode='a', header=False)

# ##########################################
# # 2nd Type:

# waveform.to_csv(path + 'waveform.csv') 
ap_data = [1, 2, 3, 4]
with 























    
    
    
    
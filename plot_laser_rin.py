# -*- coding: utf-8 -*-
"""
RIN Noise plot

Script to take the electric spectrum of laser --> PD
account the optical power and calculate and plot the RIN

Created on Fri Jan 15 15:29:47 2021

@author: Stinky
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##                          From: jan 13th
# data5_PD_13_01_2021.dat
# data6_PD_HFREQ_13_01_2021.dat
filename = 'data6_PD_HFREQ_13_01_2021.dat'

all_data = pd.read_csv(filename, sep = ';',header=None)
header_size = all_data[0] == 'Values' # last header item
header_size = np.where(header_size)[0] # array with positions of true
header_size = header_size[0] # converting first value to integer value

data = pd.read_csv(filename, sep = ';', header = header_size)
header = pd.read_csv(filename, sep = ';', header=None, nrows=header_size+1)
data.columns = ['freq','dbm','units']

# ------- Power spectrum density

# getting RBW automatically
ind = header[0]=='RBW'    # boolean state vector to find RBW
RBW = header[1].loc[ind]    # taking value in the second column
RBW = RBW.reset_index(drop=True) # resenting index to start from 0 again
RBW = float(RBW[0]) # converting string value to float


S = data.dbm - 10*np.log10(RBW) 

# ------- Calculate RIN 
opt_power = 11e-3 # W

rin = np.square(S)/ np.square(opt_power)
RIN = 10*np.log10(rin)


# ------- plot appearance
params = {'axes.labelsize': 12,
          'axes.titlesize':12,
          'xtick.labelsize':10,
          'ytick.labelsize':10,
          'axes.titlepad': 1,
          'axes.labelpad': 1,
          "text.usetex": True,
          "font.family": "serif",
          "font.sans-serif": ["Computer Modern Roman"]
          }
plt.rcParams.update(params)

# ---------figure plotting
plt.figure()
plt.plot(data.freq, data.dbm, color=[.2,.2,.2],  linewidth=0.5)

plt.grid(color=[.9,.9,.9])
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power [dBm]')
plt.xscale('log')
figure = plt.gcf()
figure.set_size_inches(4*1.4, 4)
plt.savefig(filename + '_spec.pdf', format='pdf', dpi=300)
plt.savefig(filename + '_spec.eps', format='eps', dpi=300)

# ---------spectral density plotting
plt.figure()
plt.plot(data.freq, RIN, color=[.2,.2,.2], linewidth=0.5)

plt.grid(color=[.9,.9,.9])
plt.xlabel('Frequency [Hz]')
plt.ylabel('RIN [dB/Hz]')
plt.xscale('log')
figure = plt.gcf()
figure.set_size_inches(4*1.4, 4)
plt.savefig(filename + '_RIN.pdf', format='pdf', dpi=300)
plt.savefig(filename + '_RIN.eps', format='eps', dpi=300)
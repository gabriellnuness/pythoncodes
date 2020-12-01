import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import glob


# import data and head with information
# files = glob.glob('*.dat')

filename = '10hz-10khz_1kHz_1V_funcgen.dat'

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


# RBW = 30 #hz
#getting RBW automatically
ind = header[0]=='RBW'    # boolean state vector to find RBW
RBW = header[1].loc[ind]    # taking value in the second column
RBW = RBW.reset_index(drop=True) # resenting index to start from 0 again
RBW = float(RBW[0]) # converting string value to float


S_dbm_hz = data.dbm - 10*np.log10(RBW) 

#------- plot appearance
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
plt.ylim(-110,-5)
figure = plt.gcf()
figure.set_size_inches(4*1.4, 4)
plt.savefig(filename + '_spec.pdf', format='pdf', dpi=300)
plt.savefig(filename + '_spec.eps', format='eps', dpi=300)

# ---------spectral density plotting
plt.figure()
plt.plot(data.freq, S_dbm_hz, color=[.2,.2,.2],  linewidth=0.5)

plt.grid(color=[.9,.9,.9])
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power Density [dBm/Hz]')
plt.xscale('log')
plt.ylim(-110, -5)
figure = plt.gcf()
figure.set_size_inches(4*1.4, 4)
plt.savefig(filename + '_specDensity.pdf', format='pdf', dpi=300)
plt.savefig(filename + '_specDensity.eps', format='eps', dpi=300)
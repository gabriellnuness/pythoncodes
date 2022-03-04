# -*- coding: utf-8 -*-
"""
Noise plots
Thermal + Shot + rin

To use latex fonts in the resulting figure it is necessary 
to have a functional LaTeX installation and have the python 
path pointed at it.
Otherwise, comment out the command: '"text.usetex": True'

Created on Fri Dec  4 19:58:36 2020

@author: Stinky
"""
import matplotlib.pyplot as plt
import numpy as np

k = 1.38064852 * 10**(-23)
q = 1.60217662 * 10**(-19)
T = 25 # celsius
T = T + 273.15 #kelvin
df = 1 # Hz
R = 50 #ohms
Po = np.linspace(0,10e-3,200)
n = np.ones(len(Po))
Resp = 1.03     #PD responsivity
rin_factor = 10**(-164*0.1)
Id = Resp * Po #photodiode current

therm = 4 * k * T * df/R #mean squared current
therm = therm*n #converting one value to an array

shot = 2 * q * Id * df

rin = rin_factor * Id**2 * df

###### Figure plotting and saving
params = {'axes.labelsize': 12,
          'axes.titlesize':12,
          'xtick.labelsize':10,
          'ytick.labelsize':10,
          'axes.titlepad': 1,
          'axes.labelpad': 1,
          #"text.usetex": True,
          "font.family": "serif",
          "font.sans-serif": ["Computer Modern Roman"]
          }
plt.rcParams.update(params)

plt.figure()
plt.plot(Po*1000, therm, color=[.2,.2,.2],  linewidth=1, label="Thermal noise")
plt.plot(Po*1000, shot, '--',color=[.2,.2,.2],  linewidth=1, label="Shot noise")
plt.plot(Po*1000, rin, '-.',color=[.2,.2,.2],  linewidth=1, label="rin noise")
plt.xlabel('Optical Power [mW]')
plt.ylabel(r'Mean square current [A$^2$]')
plt.legend()
# plt.grid(color=[.9,.9,.9])
plt.grid(which='minor', alpha=0.2)
plt.grid(which='major', alpha=0.5)

# # intersection between thermal and shot
# idx = np.argwhere(np.diff(np.sign(therm - shot))).flatten()
# plt.plot(Po[idx],therm[idx],'*',color=[.2,.2,.2])
# thermal_lim = Po[idx]

# # # intersection between thermal and rin
# # idx = np.argwhere(np.diff(np.sign(therm - rin))).flatten()
# # plt.plot(Po[idx],therm[idx],'ro')

# # intersection between shot and rin
# idx = np.argwhere(np.diff(np.sign(shot - rin))).flatten()
# plt.plot(Po[idx[1]],shot[idx[1]],'*',color=[.1,.1,.1])
# rin_lim = Po[idx[1]]

#save figure
figure = plt.gcf()
figure.set_size_inches(4*1.4, 4)
plt.savefig('noises.pdf', format='pdf', dpi=300, bbox_inches = 'tight',
    pad_inches = 0.1)
plt.savefig('noises.eps', format='eps', dpi=300, bbox_inches = 'tight',
    pad_inches = 0.1)
plt.show()

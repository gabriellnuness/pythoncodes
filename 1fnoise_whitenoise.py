# -*- coding: utf-8 -*-
"""
1/f noise example plot with separation from white noise source

Created on Thu Dec 10 01:45:50 2020

@author: Stinky
"""
import matplotlib.pyplot as plt
import numpy as np


#------- plot appearance
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


# creating data

f = np.arange(0.1,1e5,10)



a = 1
b = 1.2
fnoise = a/(f**b)
wnoise = 0.001*np.ones(len(f))

# ------ finding corner frequency

idx = np.argwhere(np.diff(np.sign(fnoise - wnoise))).flatten()
intersec = f[idx]


# ------plotting

fig = plt.figure()
plt.plot(f, fnoise, color=[.2,.2,.2], linestyle='dashed',linewidth=0.8,
         label='$1/f$ noise')
plt.plot(f, wnoise, color=[.2,.2,.2], 
        linestyle=(0, (3, 10, 1, 10)), #loosely dashdotted
        linewidth=0.8,
        label='White noise')
plt.plot(f[idx],fnoise[idx],'o',color=[.0,.0,.0], markersize=3)
plt.plot(f, (fnoise+wnoise), color=[.2,.2,.2])
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency [Hz]', fontsize=12)
plt.ylabel('Power Spectrum Density [dBm]', fontsize=12)

ax = fig.add_subplot(111)
ax.set_yticklabels([])
ax.set_xticks(intersec)
ax.set_xticklabels(['$f_c$'])
plt.legend()


# --------saving figure

fig.set_size_inches(4*1.4, 4)
plt.savefig('f_noise_white_noise.pdf', format='pdf', dpi=300, bbox_inches = 'tight',
    pad_inches = 0.1)
plt.savefig('f_noise_white_noise.eps', format='eps', dpi=300, bbox_inches = 'tight',
    pad_inches = 0.1)
plt.show()
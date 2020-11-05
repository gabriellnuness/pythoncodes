# -*- coding: utf-8 -*-
"""
fft and THD calculation
"""

import numpy as np
import matplotlib.pyplot as plt

# preparation for FFT
def calculate_fft(signal, time):
    n = len(signal)
    Ts = t[2] - t[1]
    fs = 1 /Ts
   
    dft = np.fft.fft(signal)
    dft = abs(dft/n) #neglecting the negative part
    dft = dft[:(n//2)] #taking frequency up to nyquist freq
    dft[1:] = 2*dft[1:] #times 2 for every frequency but the DC
    
    frequency = fs * np.arange(0, n/2) / n
    return frequency, dft

def calculate_thd(freq, dft):
        
    #taking off the offset value
    freq = frequency
    freq = freq[1:]
    dft1 = dft[1:]
    
    #separating fundamental from harmonics
    max_amp = np.max(dft1)
    max_amp_index = np.argmax(dft1)
    
    # I need to include more elements in this exclusion
    # The neighboor values are considerable to the sum as well
    # the fft is leaves a wave next to it
    fundamental = max_amp
    # fundamental_freq = freq[max_amp_index]
    
    harmonics = np.delete(dft1, max_amp_index)
    # harmonics_freq = np.delete(freq, max_amp_index)
    
    num = np.sqrt(np.sum(np.square(harmonics)))
    den = fundamental
    thd = num/den
    return thd

# fundamental
t = np.linspace(0, 1, 100000)
f = 200 #Hz
A = 50 #V
offset = 2

#harmonic noise
AA = 1 #V
ff = 1200 #Hz

noise = AA * np.sin(2 * np.pi * ff * t)
noise1 = AA/2 * np.sin(2 * np.pi * 600 * t)
signal = offset + A * np.sin(2 * np.pi * f * t) + noise  + noise1

plt.figure()
plt.plot(t, signal)
plt.xlim(0, 4/f)
plt.grid()

plt.figure()
plt.plot(t,noise)
plt.xlim(0, 4/ff)
plt.grid()

(frequency, dft) = calculate_fft(signal, t)

plt.figure()
plt.plot(dft)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [V]')
plt.xlim(-50, 1300)
plt.grid()



thd = calculate_thd(frequency, dft)

# #plot all but the offset value
# plt.figure()
# plt.plot(freq,dft1)
# plt.xlim(-50, 1300)
# plt.grid()

# #plot just the harmonics
# plt.figure()
# plt.plot(harmonics_freq,harmonics)
# plt.xlim(-50, 1300)
# plt.grid()









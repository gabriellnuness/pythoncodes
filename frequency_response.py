# -*- coding: utf-8 -*-
"""
@author: Gabriel Nunes
@date: 2020/11/04

@title: Frequency response automation

Convertion from LabVIEW code to python equivalent
"""
import pyvisa
from time import sleep
import numpy as np

oscilloscope_address = 'GPIB::1::ISNTR'
func_gen_address = 'GPIB::10::ISNTR'


initial_freq = 500 # Hz
final_freq = 5000 # Hz
freq_step = 25 # Hz
reentrance_voltage = 0.2 # Volts
saturation_voltage = 20 # maximum voltage from photodetector
voltage_step = 0.05 # Volts
max_THD = 0.03 # 0.01 = 1 %
offset = 20 #offset of the input signal 


#functions 
def in_signal_func_gen(instrument, frequency, amplitude):
    # no need to check if instrument is opened because this 
    #function is only going to be called after all 
    #the intial configurations
    instrument.write('APPLY:SIN {:.2f},{:.2f}'\
                     .format(frequency, amplitude))
        
def osc_calibration(channel):
    oscilloscope.write('*CLS')
    oscilloscope.chunk_size = 512
    sleep(10)
    
    oscilloscope.write(':CHANnel{:d}:RANGe {:d}'\
                       .format(channel,saturation_voltage))
    sleep(10)
    
    time_scale = (1 / frequency) * 5 # 5 times the period
    oscilloscope.write(':TIMebase:RANGe {:.4f}'\
                       .format(time_scale))
    sleep(10)
    
    oscilloscope.write('CHANnel{:d}:OFFSet {:d}'\
                       .format(channel, offset))
    sleep(10)
    
    oscilloscope.write(':MEASure:SOURce\sCHANnel{:d}'\
                       .format(channel))
    sleep(700) #critical delay to wait the measurement
    
    # begin fine adjustment
    oscilloscope.write(':MEASure:VMAX?')
    sleep(50)
    osc_max = oscilloscope.read()
    oscilloscope.write(':MEASure:VMIN?')
    sleep(50)
    osc_min = oscilloscope.read()
    
    volt_scale = (osc_max - osc_min) / 4 * 8 #fills 1/2 of the screen
    oscilloscope.write(':CHANnel{:d}:RANGe {:.4f}'\
                       .format(channel, volt_scale))
    sleep(10)
    
    osc_offset = (osc_max + osc_min) / 2
    oscilloscope.write(':CHANnel{:d}:OFFSet {:.4f}'\
                       .format(channel, osc_offset))
    oscilloscope.write('*CLS')
    
    
def osc_measurement():
    if oscilloscope.query(':ACQuire:TYPE?') == 'AVERage':
        oscilloscope.write(':DIGitize CHAN1')
        osc_response = oscilloscope.read()
    elif oscilloscope.query(':ACQuire:TYPE?') == 'NORMal':
        oscilloscope.write(':SINGle CHAN1')
        osc_response = oscilloscope.read()
    return(osc_response)

def calculate_fft(signal, time):
    n = len(signal)
    Ts = time[2] - time[1]
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
    

## Basic documentation for pyvisa
# rm.list_resources()
#define instrument address
# inst = rm.open_resource('GPIB0::12::INSTR') 
# inst.query("*IDN?") # send msg and read response instantly
# inst.write('message') # send msg
# inst.read()   #read msg
# inst.wait_for_srq()

rm = pyvisa.ResourceManager()   #initialize VISA communication

# oscilloscope initialization and initial configuration
oscilloscope = rm.open_resource(oscilloscope_address)
oscilloscope.write('*rst')
oscilloscope.write(':TIMEBASE:MODE MAIN') #MAIN, ROLL, XY, WIND
oscilloscope.write(':ACQuire:TYPE AVERage') #NORMal, AVERage, HRESolution, PEAK
oscilloscope.write(':ACQuire:COUNt 8') #from 2 to 65536
oscilloscope.write(':TRIGGER:EDGE:SOURCE CHANnel2')
oscilloscope.write('CHANnel1:PROBe 1')  #interferometer received signal
oscilloscope.write('CHANnel2:PROBe 1')  #modulation inserted signal
oscilloscope.write_termination = '\n'
oscilloscope.timeout = 20

# function generator initialization and configuration
func_gen = rm.open_resource(func_gen_address) #instrument definition
func_gen.timeout = 20


iterations = (final_freq - initial_freq) / freq_step

for i in iterations:
    frequency = initial_freq + freq_step * i
    amplitude = saturation_voltage
    in_signal_func_gen(func_gen, frequency, amplitude)  #apply signal
    
    #check how data is going to be acquired to later adjust it
    data, data_time = osc_measurement(1)
    frequency, dft = calculate_fft(data, data_time) # calculate fft before thd
    thd = calculate_thd(frequency, dft)   # calculate actual THD
    
    while thd > max_THD:       
        amplitude = amplitude - voltage_step    #reduces the applied voltage
        in_signal_func_gen(func_gen, frequency, amplitude)
        
        data, data_time = osc_measurement(1)
        frequency, dft = calculate_fft(data, data_time) # calculate fft before thd
        thd = calculate_thd(frequency, dft)   # calculate actual THD
    
    osc_calibration(1)
    osc_calibration(2)
    data, data_time = osc_measurement(1)
    
    #save file with entire waveform
    #append to another file with just the Vin, max, min, thd, etc...








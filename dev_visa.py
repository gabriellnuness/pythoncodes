# -*- coding: utf-8 -*-
"""
test visa functions
"""

import pyvisa
from time import sleep
import numpy as np

oscilloscope_address = 'GPIB0::1::INSTR'
func_gen_address = 'GPIB0::10::INSTR'

# Data acquirement settings
initial_freq = 30 # Hz
final_freq = 5000 # Hz
freq_step = 25 # Hz
reentrance_voltage = 5 # Volts
saturation_voltage = 20 # maximum voltage from photodetector
voltage_step = 0.05 # Volts
max_THD = 0.03 # 0.01 = 1 %
offset = 20 #offset of the input signal 
offset_interf = 0


def in_signal_func_gen(instrument, frequency, amplitude):
    # no need to check if instrument is opened because this 
    #function is only going to be called after all 
    #the intial configurations
    instrument.write('APPLY:SIN {:.2f},{:.2f}'\
                     .format(frequency, amplitude))

def osc_calibration(channel):
    oscilloscope.write('*CLS')
    # oscilloscope.chunk_size = 512
    sleep(0.1)
    oscilloscope.write(':WAVeform:SOURce CHANnel{:d}'\
                       .format(channel))#selecting channel
    sleep(0.1)    
    oscilloscope.write(':CHANnel{:d}:RANGe {:d}'\
                       .format(channel,saturation_voltage))
    sleep(0.1)
    
    time_scale = (1 / frequency) * 5 # 5 times the period
    oscilloscope.write(':TIMebase:RANGe {:.4f}'\
                       .format(time_scale))
    sleep(0.1)
    
    if channel == 1:
        oscilloscope.write('CHANnel{:d}:OFFSet {:d}'\
                           .format(channel, offset_interf))
    elif channel == 2:
        oscilloscope.write('CHANnel{:d}:OFFSet {:d}'\
                           .format(channel, offset))
    sleep(0.1)
    
    # oscilloscope.write(':MEASure:SOURce\sCHANnel{:d}'\
    #                    .format(channel))
    oscilloscope.write(':DIGitize')
        
    sleep(0.7) #critical delay to wait the measurement
    
    # begin fine adjustment
    osc_max = oscilloscope.query(':MEASure:VMAX? CHANnel{:d}'\
                                 .format(channel))
    sleep(0.5)
    osc_min = oscilloscope.query(':MEASure:VMIN? CHANnel{:d}'\
                                 .format(channel))
    
    volt_scale = (float(osc_max) - float(osc_min)) / 6 * 8 #fills 6/8 of the screen
    oscilloscope.write(':CHANnel{:d}:RANGe {:.4f}'\
                       .format(channel, volt_scale))
    sleep(0.5)
    
    osc_offset = (float(osc_max) + float(osc_min)) / 2
    oscilloscope.write(':CHANnel{:d}:OFFSet {:.4f}'\
                        .format(channel, osc_offset))
    oscilloscope.write('*CLS')
    oscilloscope.write(':RUN')
        
def osc_measurement(channel):
    if oscilloscope.query(':ACQuire:TYPE?') == 'AVERage':
        
        oscilloscope.write('WAVeform:FORmat ASCII') #BYTE|ASCII|WORD
        oscilloscope.write(':DIGitize CHAN{:d}'.format(channel)) #just channel 1 will appear
        osc_response = oscilloscope.read()
       #send query with  :WAVeform:DATA?
       
    elif oscilloscope.query(':ACQuire:TYPE?') == 'NORMal':
        oscilloscope.write(':SINGle CHAN{:d}'.format(channel))
        osc_response = oscilloscope.read() # probably wrong
    return(osc_response)    


    
rm = pyvisa.ResourceManager()   #initialize VISA communication
devices = rm.list_resources()

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
oscilloscope.write('CHANnel1:DISPlay ON')
oscilloscope.write('CHANnel2:DISPlay ON')
oscilloscope.write(':TRIGger:EDGE:SOURce CHANnel2')
oscilloscope.write(':TRIGger:EDGE:LEVel {:d}'.format(offset))
oscilloscope.timeout = 20

# function generator initialization and configuration
func_gen = rm.open_resource(func_gen_address) #instrument definition
func_gen.timeout = 20

#TEST FUNCTION GENERATOR -WORKS!!
frequency = initial_freq
amplitude = reentrance_voltage
in_signal_func_gen(func_gen,frequency,amplitude)

#TEST OSCILLOSCOPE CALIBRATION -WORKS!!
osc_calibration(2)
osc_calibration(1)


data = osc_measurement(2)
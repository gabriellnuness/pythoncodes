# -*- coding: utf-8 -*-
"""
test visa functions
"""

import pyvisa
from time import sleep
import numpy as np
import pandas as pd

def wait_srq(time):
    # time in milliseconds
    stb = pyvisa.read_stb()
    while stb == 0:
        sleep(time)
    


osa_address = 'GPIB1::9::INSTR'

rm = pyvisa.ResourceManager()   #initialize VISA communication
devices = rm.list_resources()

# oscilloscope initialization and initial configuration
osa = rm.open_resource(osa_address)
osa.write_termination = '\n'
osa.timeout = 20

osa.write('MEA0') #single read command

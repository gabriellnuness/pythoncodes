# this scripts import the plotting script and run to all files in folder 
# with .dat format

import plot_elec_spectrum
import glob 


files = glob.glob('*.dat')

for filename in files:
    plot_elec_spectrum.main(filename)
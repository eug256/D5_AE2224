# to do in this file:
# - iterate over all the samples
# - calculate the frequencies

from pathlib import Path

import sys
import vallenae as vae
import os
import math
import time

from scipy.fft import fft, fftfreq
import numpy as np

import matplotlib.pyplot as plt
import pandas as pd

# put the pridb and tradb in the same folder as this python file

HERE = Path(__file__).parent if "__file__" in locals() else Path.cwd()
PRIDB = os.path.join(HERE, "1p12_Ft_25000.pridb")
TRADB = os.path.join(HERE, "1p12_Ft_25000.tradb")

# load the data

pridb = vae.io.PriDatabase(PRIDB)
tradb = vae.io.TraDatabase(TRADB)

def fourierT(y,t):
    yf = fft(y)
    dt = t[1] - t[0]
    freq = fftfreq(len(y), dt)
    freq_0 = []
    amplitude_spectrum_0 = []
    amplitude_spectrum = 2*np.abs(yf)
    for i in range(len(freq)):
        if freq[i] >= 0:
            freq_0.append(freq[i])
            amplitude_spectrum_0.append(amplitude_spectrum[i])

    return freq_0, amplitude_spectrum_0


if __name__ == '__main__':

    first_time = True

    #specify time to run in seconds
    runtime = 60

    start = time.time()

    run = True
    while run:
        try:
            existing_file = pd.read_csv('peaks.csv')
            last_entry = existing_file["trai"].iloc[-1]
            samples = range(last_entry+1,last_entry+10001)
            first_time = False
        except:
            samples = range(1,10000)
            
        peak_frequencies = []
        
        for n in samples:
            try:
                df_hits = pridb.iread_hits(query_filter=f"TRAI = {n}")
            except:
                run = False
            y,t = tradb.read_wave(n)
            
            a,b = fourierT(y,t)
            
            PeakFreq = a[b.index(max(b))]
            peak_frequencies.append(PeakFreq)
            
            if n%1000 == 0:
                print(n)
                
        peak_frequencies = pd.DataFrame({"trai": samples, "peak_frequencies": peak_frequencies})
        if first_time:
            peak_frequencies.to_csv('peaks.csv', mode='a', index=False)
        else:
            peak_frequencies.to_csv('peaks.csv', mode='a', index=False, header=False)

        now = time.time()
        if now-start >= runtime:
            run = False


        
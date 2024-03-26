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
from threading import Thread
from itertools import chain

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

def Calculate(samples):
    peak_frequencies = []
        
    for n in samples:
        try:
            df_hits = pridb.iread_hits(query_filter=f"TRAI = {n}")
            y,t = tradb.read_wave(n)
            a,b = fourierT(y,t)
        
            PeakFreq = a[b.index(max(b))]
            peak_frequencies.append(PeakFreq)
        except:
            peak_frequencies.append(0)

        if n%1000 == 0:
            print(n)

    #results[index]= peak_frequencies
    return peak_frequencies
            
def main():
    #specify time to run in seconds
    runtime = 10 * 60

    first_time = True
    start = time.time()

    run = True
    while run:

        try:
            existing_file = pd.read_csv('peaks.csv')
            last_entry = existing_file["trai"].iloc[-1]
            length = 10000
            samples = range(last_entry+1,last_entry+1+length)
            first_time = False
        except:
            samples = range(1,10001)

        """
        nt = 6

        threads = [None]*nt
        results = [None]*nt

        try:
            existing_file = pd.read_csv('peaks.csv')
            last_entry = existing_file["trai"].iloc[-1]
            samples = []
            length = 1000
            for i in range(nt):
                sample = range(last_entry+1+(i*length),last_entry+1+length+(i*length))
                samples.append(sample)
            first_time = False
        except:
            samples = []
            length = 10000
            for i in range(nt):
                sample = range(1+(i*length),1+length+(i*length))
                samples.append(sample)

        for i in range(len(threads)):
            threads[i] = Thread(target=Calculate, args=(samples[i], results, i))
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()

        peak_frequencies = list(chain(*results))

        samples = list(chain(*samples))
        """

        peak_frequencies = Calculate(samples)

        peak_frequencies = pd.DataFrame({"trai": samples, "peak_frequencies": peak_frequencies})
        if first_time:
            peak_frequencies.to_csv('peaks.csv', mode='a', index=False)
        else:
            peak_frequencies.to_csv('peaks.csv', mode='a', index=False, header=False)
            
        now = time.time()
        timeleft = round(runtime - now + start, 1)
        if timeleft >= 0:
            print(f"{timeleft}s of runtime left")
        if timeleft <= 0:
            run = False

if __name__ == '__main__':
        main()
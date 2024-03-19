# to do in this file:
# - create a clear structure with functions and such
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

df_hits = pridb.iread_hits(query_filter="TRAI = 1")

y, t = tradb.read_wave(1)

# reduce the size of the signal

duration = [item[4] for item in df_hits][0]

margin = 50
    
start = np.where(t == 0)[0][0]
start -= margin
end = np.where(t >= duration)[0][0]
end += margin

# truncate the signal to only include the duration with some margin

"""
y = y[start:end]
t = t[start:end]
"""

# calculate the fft

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

# plotting the fft with pyplot

plt.figure()
plt.plot(freq_0, amplitude_spectrum_0)
plt.show()
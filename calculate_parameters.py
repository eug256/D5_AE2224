import yaml
import vallenae as vae
import numpy as np
from scipy.fft import fft, fftfreq
import csv


with open('settings.yml', 'r') as file:
    results = yaml.safe_load(file)
    TRADB = results['tradb']
    PRIDB = results['pridb']
    
################## INPUT: ###################
trai = [1,10000]
#############################################
trai_min = min(trai)
trai_max = max(trai)

pridb = vae.io.PriDatabase(PRIDB)
df_hits = pridb.iread_hits(query_filter=f"TRAI >= {trai_min} AND TRAI <= {trai_max}")
fields = ['Amplitude', 'Energy', 'Rise_time', 'Count_(log10)', 'Max_freq', 'Variance'] 
total_data = []

for i in df_hits:
    with vae.io.TraDatabase(TRADB) as tradb:
        y, t = tradb.read_wave(i[12])
        
    yf = fft(y)
    dt = t[1] - t[0]
    freq = fftfreq(len(y), dt)
    freq_0 = []
    amplitude_spectrum_0 = []
    amplitude_spectrum = 2*np.abs(yf)
    for j in range(len(freq)):
        if freq[j] >= 0:
            freq_0.append(freq[j])
            amplitude_spectrum_0.append(amplitude_spectrum[j])
    
    total_data.append([i[3],i[5],i[9],np.log10(i[11]),max(amplitude_spectrum_0),round(np.var(y)*10**10,2)])

    
with open(f'{trai_min}-{trai_max}.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
     
    write.writerow(fields)
    write.writerows(total_data)
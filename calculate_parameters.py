import yaml
import vallenae as vae
import numpy as np
from scipy.fft import fft, fftfreq
import csv
def parameters(trai_start,trai_end):
    with open('settings.yml', 'r') as file:
        results = yaml.safe_load(file)
        TRADB = results['tradb']
        PRIDB = results['pridb']
        
    ################## INPUT: ###################
    trai = [trai_start,trai_end]
    #############################################
    trai_min = min(trai)
    trai_max = max(trai)

    pridb = vae.io.PriDatabase(PRIDB)
    df_hits = pridb.iread_hits(query_filter=f"TRAI >= {trai_min} AND TRAI <= {trai_max}")
    fields = ['Amplitude', 'Energy', 'Rise_time', 'Count', 'Max_freq', 'Variance'] 
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
        
        total_data.append([i[3],i[5],i[9],i[11],max(amplitude_spectrum_0),round(np.var(y)*10**10,3)])
    return total_data

def parameters_filtering(trai_start,trai_end):
    with open('settings.yml', 'r') as file:
        results = yaml.safe_load(file)
        TRADB = results['tradb']
        PRIDB = results['pridb']
        
    ################## INPUT: ###################
    trai = [trai_start,trai_end]
    #############################################
    trai_min = min(trai)
    trai_max = max(trai)

    pridb = vae.io.PriDatabase(PRIDB)
    df_hits = pridb.iread_hits(query_filter=f"TRAI >= {trai_min} AND TRAI <= {trai_max}")
    fields = ['Amplitude', 'Energy', 'Rise_time', 'Count', 'Max_freq', 'Variance',"Counts/RT"] 
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
        
        total_data.append([i[3],i[5],i[9],i[11],max(amplitude_spectrum_0),round(np.var(y)*10**10,3),i[11]/i[9]])
    return total_data
""" 
with open(f'{trai_min}-{trai_max}.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
     
    write.writerow(fields)
    write.writerows(total_data)
"""  
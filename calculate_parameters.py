import yaml
import vallenae as vae
import numpy as np
from scipy.fft import fft, fftfreq
import csv
import os
import pandas as pd
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
    df_hits = new_func(trai_min, trai_max, pridb) 
    fields = ['Amplitude', 'Energy', 'Rise_time', 'Count', 'Max_freq', 'Variance'] 
    total_data = []

    for i in df_hits:
        with vae.io.TraDatabase(TRADB) as tradb:
            y, t = tradb.read_wave(i[12])

        max_amplitude = max(np.abs(y)) 
        yf = fft(y)
        dt = t[1] - t[0]
        freq = fftfreq(len(y), dt)
        freq_0 = freq[freq >= 0]
        amplitude_spectrum = 2 * np.abs(yf)
        amplitude_spectrum_0 = amplitude_spectrum[freq >= 0]

        total_data.append([max_amplitude, i[5], i[9], i[11], freq_0[np.argmax(amplitude_spectrum_0)], round(np.var(y) * 10 ** 10, 3), i[11] / i[9]])
    return total_data

def new_func(trai_min, trai_max, pridb):
    df_hits = pridb.iread_hits(query_filter=f"TRAI >= {trai_min} AND TRAI <= {trai_max}")
    return df_hits

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

        max_amplitude = max(np.abs(y))
        yf = fft(y)
        dt = t[1] - t[0]
        freq = fftfreq(len(y), dt)
        freq = fftfreq(len(y), dt)
        freq_0 = freq[freq >= 0]
        amplitude_spectrum = 2 * np.abs(yf)
        amplitude_spectrum_0 = amplitude_spectrum[freq >= 0]
        total_data.append([max_amplitude, i[5], i[9], i[11], freq_0[np.argmax(amplitude_spectrum_0)], round(np.var(y) * 10 ** 10, 3), i[11] / i[9]])
    return total_data

def calculate_stuff(trai_start,trai_end):
    with open('settings.yml', 'r') as file:
        results = yaml.safe_load(file)
        TRADB = results['tradb']
        PRIDB = results['pridb']

    trai_min = trai_start
    trai_max = trai_end
    
    pridb = vae.io.PriDatabase(PRIDB)
    df_hits = pridb.iread_hits(query_filter=f"TRAI >= {trai_min} AND TRAI <= {trai_max}")

    total_data = []

    for i in df_hits:
        print(i)
        with vae.io.TraDatabase(TRADB) as tradb:
            y, t = tradb.read_wave(int(i[12]))
    
            
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
        
        total_data.append([max(np.abs(y)),freq_0[np.argmax(amplitude_spectrum_0)],i[4],i[5],i[6],i[9],i[11]])
    
    with open(f'{trai_min}-{trai_max}-full.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
        write = csv.writer(f)
        
        write.writerow(['amplitude','frequency','duration','energy','rms','rise_time','counts'])
        write.writerows(total_data)

def calc_counts_per_rise_time(trai_min,trai_max):
    HERE = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    DATA = os.path.join(HERE, f"{trai_min}-{trai_max}-full.csv")

    df = pd.read_csv(DATA) # read data
    df = df.assign(cprt=df["counts"]/df["rise_time"])
    df.to_csv(f"{trai_min}-{trai_max}-full.csv",index=False)

if __name__ == '__main__':
    #calculate_stuff(1,100000)
    calc_counts_per_rise_time(1,100000)
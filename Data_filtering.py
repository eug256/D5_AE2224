import yaml
import vallenae as vae
import numpy as np
from scipy.fft import fft, fftfreq
import csv
import os
import pandas as pd

def decide(array):

    # features to take into account, maybe change this later if not good
    var = array[7]
    counts = array[6]
    # look at variance first: hard limit
    if var < 8:
        return False
    
    # now counts/rise time: hard limit
    if counts == 0: # change this:
        return False
    
    return True

def calc_filter_data(trai_start,trai_end):
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
        #print(i)
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
        variance = round(np.var(y) * 10**10)
        feature_array = [max(np.abs(y)), freq_0[np.argmax(amplitude_spectrum_0)], i[4], i[5], i[6], i[9], i[11], variance]

        if decide(feature_array) is True:
            total_data.append(feature_array)
    
    with open(f'{trai_min}-{trai_max}-filtered.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
        write = csv.writer(f)
        
        write.writerow(['amplitude','frequency','duration','energy','rms','rise_time','counts'])
        write.writerows(total_data)

calc_filter_data(1,10000)

# if __name__ == "__main__":
    # data = filter_dataset(1, 5)
    # new_data = np.zeros((5,7))

    # new_data = np.array(params(1,2)) # [amplitude, energy, rise time, counts, max amplitude in the freq spectrum, variance, counts/rise time]
    # new_data[0] = data[0]
    # print(data)
    # print(new_data)
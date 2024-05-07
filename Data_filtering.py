import yaml
import vallenae as vae
import numpy as np
from scipy.fft import fft, fftfreq
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import time

def decide(array):

    # features to take into account, maybe change this later if not good
    #var = array[7]
    counts = array[5]
    energy = array[2]

    # look at counts:
    if counts >= 3 and energy >= 85.15572: # change this:
        return True
    else:
        return False

def calc_filter_data(trai_start,trai_end):
    with open('settings.yml', 'r') as file:
        results = yaml.safe_load(file)
        TRADB = results['tradb']
        PRIDB = results['pridb']

    trai_min = trai_start
    trai_max = trai_end
    
    pridb = vae.io.PriDatabase(PRIDB)
    #df_hits = pridb.iread_hits()
    df_hits = pridb.iread_hits(query_filter=f"TRAI >= {trai_start} AND TRAI <= {trai_end}")

    time0 = time.time()

    total_data = []
    counter = trai_start
    counter_list =[]


    for i in df_hits:
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
        feature_array = [max(np.abs(y)),i[4],i[5],i[6],i[9],i[11],freq_0[np.argmax(amplitude_spectrum_0)],i[12]]
        
        if decide(feature_array) == True:
            total_data.append(feature_array)
            counter_list.append(counter)
        counter +=1
        if counter%1000 == 0:
            print(counter)

    time1 = time.time()
    
    with open(f'{trai_min}-{trai_max}-filtered-new.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(['amplitude','duration','energy','rms','rise time','counts','peak frequency','trai'])
        write.writerows(total_data)
    
    print(round(time1-time0))

def calc_variance(trai_start,trai_end):

    with open('settings.yml', 'r') as file:
        results = yaml.safe_load(file)
        TRADB = results['tradb']
        PRIDB = results['pridb']
    
    pridb = vae.io.PriDatabase(PRIDB)
    df_hits = pridb.iread_hits(query_filter=f"TRAI >= {trai_start} AND TRAI <= {trai_end}")

    var = []

    for i in df_hits:
        with vae.io.TraDatabase(TRADB) as tradb:
            y, t = tradb.read_wave(int(i[12]))

        variance = np.var(y) * 10**10
        if i[11] >= 3:
            var.append(variance)

    print("Mean variance: ", np.mean(var))
    print("30th percentile: ", np.percentile(var,30))

    return var

def calc_energy(trai_start,trai_end):

    with open('settings.yml', 'r') as file:
        results = yaml.safe_load(file)
        TRADB = results['tradb']
        PRIDB = results['pridb']
    
    pridb = vae.io.PriDatabase(PRIDB)
    df_hits = pridb.iread_hits(query_filter=f"TRAI >= {trai_start} AND TRAI <= {trai_end}")

    E = []

    for i in df_hits:
        if i[11] >= 3:
            E.append(i[5])
    
    print(len(E))
    tp = np.percentile(E,30)
    return tp

calc_filter_data(5500000,5600000)
print("one done")
calc_filter_data(5600000,5700000)
print("two done")
calc_filter_data(5700000,5800000)
print("all three done")

#the thirtieth percentile of all the waves (up to 15.4 million) is 85.15572




    
"""
plt.figure(figsize=(30,20))

for n in range(1,16):
    #var = calc_variance(n*mil,n*mil+sample_size)
    E = calc_energy(n*mil,n*mil+sample_size)
    plt.subplot(5,3,n)
    plt.title(f"{n}")
    plt.xlim(0,3000)
    print(n)
    plt.hist(E,50)

plt.show()

"""

# if __name__ == "__main__":
    # data = filter_dataset(1, 5)
    # new_data = np.zeros((5,7))

    # new_data = np.array(params(1,2)) # [amplitude, energy, rise time, counts, max amplitude in the freq spectrum, variance, counts/rise time]
    # new_data[0] = data[0]
    # print(data)
    # print(new_data)
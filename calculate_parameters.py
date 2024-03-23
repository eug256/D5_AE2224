import yaml
import vallenae as vae
import numpy as np
from scipy.fft import fft, fftfreq
import csv
import time
import multiprocessing
import pandas as pd
import os

def parameters(trai_start, trai_end, create_csv=False, timer=False):
    if timer == True:
        start = time.time()
    with open('settings.yml', 'r') as file:
        results = yaml.safe_load(file)
        TRADB = results['tradb']
        PRIDB = results['pridb']

    trai_min = trai_start
    trai_max = trai_end

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
        
        total_data.append([i[3],i[5],i[9],i[11],max(amplitude_spectrum_0),round(np.var(y)*10**10,2)])
    
    if create_csv == True:
        with open(f'{trai_min}-{trai_max}.csv', 'w', newline='') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            
            write.writerow(fields)
            write.writerows(total_data)
    if timer == True:
        end = time.time()
        print(end - start)
    
    return total_data

def merge_csv(trai_start, trai_end, csv_files):
    df_csv_concat = pd.concat([pd.read_csv(file) for file in csv_files ], ignore_index=True)
    df_csv_concat.to_csv(f"{trai_start}-{trai_end}.csv",index=False)
    for file in csv_files:
        os.remove(file)

def run(trai_start, trai_end, create_csv=False, timer=False, number_of_threads=1):
    if multiprocessing.cpu_count() < number_of_threads:
        print(f"Maximum number of threads is {multiprocessing.cpu_count()}")
        quit()
    processes = {}

    number_of_trai = int((trai_end-trai_start+1)/number_of_threads)
    actual_start = trai_start
    actual_end = number_of_trai

    csv_files = []

    for index in range(number_of_threads):
        csv_files.append(f"{actual_start}-{actual_end}.csv")
        processes[index] = multiprocessing.Process(target=parameters, args=(actual_start, actual_end, True, timer)) 
        actual_start += number_of_trai
        actual_end += number_of_trai
    for index in range(number_of_threads):
        processes[index].start()
    for index in range(number_of_threads):
        processes[index].join()

    merge_csv(trai_start,trai_end,csv_files)
    

if __name__ == '__main__':
    run(1, 1000, True, True, 4)
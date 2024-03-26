import sys
import vallenae as vae
import pandas as pd
import numpy as np
from calculate_parameters import parameters_filtering as params

def decide(array):

    # features to take into account, maybe change this later if not good
    var = array[5]
    cprt = array[6]
    # en = array[1]

    # look at variance first: hard limit
    if var < 8:
        return False
    
    # now counts/rise time: hard limit
    if cprt == 0: # change this:
        return False
    
    return True

def filter_dataset(trai_start, trai_end, previous_last_trai = 1):

    # get raw data and change it to numpy array
    unfiltered_data = params(trai_start, trai_end * 3) # would rather generate dynamically but it takes ages to run
    unfiltered_data = np.array(unfiltered_data)

    # deterime the shape of the output array: (desired nr of waveforms, nr of parameters)
    nr_param = unfiltered_data.shape[1]
    nr_trai = trai_end - trai_start + 1

    # generate array for filtered data
    filtered_data = np.zeros((nr_trai, nr_param))

    current_trai = 0
    i = 1
    while True:
        array = unfiltered_data[i]
        if decide(array) == False:
            i+=1
        else:
            filtered_data[current_trai] = array
            current_trai+=1
            i+=1
        if current_trai == nr_trai:
            break

    return filtered_data, i # return filtered array and last trai number in the original dataset

# data = filter_dataset(1, 5)
# new_data = np.zeros((5,7))

# data = np.array(params(1,2)) # [amplitude, energy, rise time, counts, max amplitude in the freq spectrum, variance, counts/rise time]
# new_data[0] = data[0]
# print(data)
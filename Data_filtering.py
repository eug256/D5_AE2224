import sys
import vallenae as vae
import pandas as pd
import numpy as np
from calculate_parameters import parameters

def filter(trai_start, trai_end):
    unfiltered_data = parameters(trai_start, trai_end)

    return unfiltered_data

data = filter(1, 1000)

data = np.array(data)

print("fuck")
print(data.shape)
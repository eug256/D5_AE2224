import cowsay
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

X = [0, 1] # get some array

# split into train and test here

# kmeans = KMeans(n_clusters = 3, random_state = 0, n_init= "auto").fit(X_train)

# y = kmeans.predict


print(cowsay.cow("Fuck"))
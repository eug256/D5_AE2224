from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import os
from plotnine import *

HERE = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
DATA = os.path.join(HERE, "1-10000-amp-freq.csv")

X = pd.read_csv(DATA) # read data
X_scaled = StandardScaler().fit(X).transform(X) # transform data (standardize so all columns have zero mean and unit variance)

kmeans = KMeans(n_clusters = 4, random_state = 0, n_init= "auto").fit(X) # apply kmeans

X['_cluster'] = pd.Categorical(kmeans.labels_) # read clusters from kmeans

p = ( 
    ggplot(X, aes('frequency', 'amplitude', color = '_cluster')) +\
    geom_point() +\
    labs(title = "Cluster by amplitude and frequency, k=4")
)
print(p) # plot clusters
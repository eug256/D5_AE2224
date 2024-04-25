import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN 
from plotnine import *
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import numpy as np


HERE = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
DATA = os.path.join(HERE, "1-10000-filtered.csv")

X = pd.read_csv(DATA) # read data
#X = X.loc[(X['frequency'] >= 125000) & (X['frequency'] <= 150000)]
X_scaled = StandardScaler().fit(X).transform(X)

EPS=22
SAMPLES=150

neighbors = NearestNeighbors(n_neighbors=SAMPLES)
neighbors_fit = neighbors.fit(X)
distances, indices = neighbors_fit.kneighbors(X)

distances = np.sort(distances, axis=0)
distances = distances[:,1]
plt.plot(distances)

db = DBSCAN(eps=EPS, min_samples=SAMPLES).fit(X)
labels = db.labels_
X["_labels"] = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)


X = X.loc[(X['_labels'] >= 0)]

plot = ( 
    ggplot(X, aes('frequency', 'amplitude', color = '_labels')) +\
    geom_point() +\
    labs(title = f"Cluster by amplitude and frequency, k={n_clusters_}, dbscan")
)
print(plot)

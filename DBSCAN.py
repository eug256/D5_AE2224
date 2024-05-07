import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN 
from plotnine import *
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import numpy as np
import math
distances_total = []
HERE = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
DATA = os.path.join(HERE, "5700000-5800000-filtered.csv")

X = pd.read_csv(DATA) # read data

#X = X.loc[(X['frequency'] >= 125000) & (X['frequency'] <= 150000)]
X_scaled = StandardScaler().fit(X).transform(X)
X_scaled = X_scaled[:, : 6]
#print(X_scaled)

SAMPLES=7

neighbors = NearestNeighbors(n_neighbors=SAMPLES)
neighbors_fit = neighbors.fit(X_scaled)
distances, indices = neighbors_fit.kneighbors(X_scaled)

distances = np.sort(distances, axis=0)
for i in range(len(distances)):
    distances_total.append(np.sqrt(np.sum(distances[i,:]**2)))

plt.plot(distances_total)
plt.show()

angular_variation = np.diff(distances_total, 1000)

knee_index = np.argmax(angular_variation) + 2

EPS = distances_total[knee_index]

print("Calculated eps value:", EPS)


db = DBSCAN(eps=EPS, min_samples=SAMPLES).fit(X_scaled)
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
plot.show()

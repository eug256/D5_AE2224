import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN 
from plotnine import *
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import numpy as np


HERE = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
DATA = os.path.join(HERE, "1-10000-full-pca.csv")
DATA2 = os.path.join(HERE, "1-10000-full.csv")

X2 = pd.read_csv(DATA2) # read data
X = pd.read_csv(DATA) # read data
#X = X.loc[(X['frequency'] >= 125000) & (X['frequency'] <= 150000)]
X_scaled = StandardScaler().fit(X).transform(X)

EPS=0.466
SAMPLES=10

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
print(X['_labels'])

X2 = X2.assign(_labels=X['_labels'])
#X = X.loc[(X['_labels'] >= 0)]

plot = ( 
    ggplot(X2, aes('frequency', 'amplitude', color = '_labels')) +\
    geom_point() +\
    labs(title = f"Cluster by amplitude and frequency, k={n_clusters_}, dbscan")
)
plot2 = ( 
    ggplot(X, aes('0', '1', color = '_labels')) +\
    geom_point() +\
    labs(title = f"Cluster by pc0 and pc1, k={n_clusters_}, pca")
)
print(plot)
print(plot2)

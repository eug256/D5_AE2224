from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
import pandas as pd
from plotnine import *
import os

HERE = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
DATA = os.path.join(HERE, "1-10000-amp-freq.csv")

X = pd.read_csv(DATA) # read data
X_filter = X.loc[(X['frequency'] >= 125000) & (X['frequency'] <= 150000)]

X_scaled = StandardScaler().fit(X_filter).transform(X_filter) # transform data (standardize so all columns have zero mean and unit variance)

clustering_ward = AgglomerativeClustering(9,linkage='ward').fit(X_scaled)

X_filter['_cluster_ward'] = pd.Categorical(clustering_ward.labels_) # read clusters from kmeans

p_ward = ( 
    ggplot(X_filter, aes('frequency', 'amplitude', color = '_cluster_ward')) +\
    geom_point() +\
    labs(title = "Cluster by amplitude and frequency, k=9, ward")
)

print(p_ward)

clustering_complete = AgglomerativeClustering(9,linkage='complete').fit(X_scaled)

X_filter['_cluster_complete'] = pd.Categorical(clustering_complete.labels_) # read clusters from kmeans

p_complete = ( 
    ggplot(X_filter, aes('frequency', 'amplitude', color = '_cluster_complete')) +\
    geom_point() +\
    labs(title = "Cluster by amplitude and frequency, k=9, complete")
)

print(p_complete)

clustering_average = AgglomerativeClustering(9,linkage='average').fit(X_scaled)

X_filter['_cluster_average'] = pd.Categorical(clustering_average.labels_) # read clusters from kmeans

p_average = ( 
    ggplot(X_filter, aes('frequency', 'amplitude', color = '_cluster_average')) +\
    geom_point() +\
    labs(title = "Cluster by amplitude and frequency, k=9, average")
)

print(p_average)

clustering_single = AgglomerativeClustering(4,linkage='single').fit(X_scaled)

X_filter['_cluster_single'] = pd.Categorical(clustering_single.labels_) # read clusters from kmeans

p_single = ( 
    ggplot(X_filter, aes('frequency', 'amplitude', color = '_cluster_single')) +\
    geom_point() +\
    labs(title = "Cluster by amplitude and frequency, k=9, single")
)

print(p_single)
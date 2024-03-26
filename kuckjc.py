from sklearn.cluster import DBSCAN 
from calculate_parameters import parameters
from matplotlib import pyplot as plt
import matplotlib
from sklearn.neighbors import NearestNeighbors
import numpy as np
from Data_filtering import filter_dataset
trai_start = 1
trai_end = 1000
#df = parameters(trai_start,trai_end)
df = filter_dataset(trai_start,trai_end)[0]
df=df[:,[0,1,2,3,4,5]]
# Initialize NearestNeighbors class
neigh = NearestNeighbors(n_neighbors=2)
nbrs = neigh.fit(df)
distances, indices = nbrs.kneighbors(df)

# Plotting K-distance Graph
distances = np.sort(distances, axis=0)
distances = distances[:,1]

plt.figure(figsize=(20,10))
plt.plot(distances)
plt.title('K-distance Graph',fontsize=20)
plt.xlabel('Data Points sorted by distance',fontsize=14)
plt.ylabel('Epsilon',fontsize=14)
plt.show()

# Initialize DBSCAN with desired parameters
eps = 22 # Adjust according to your dataset
min_samples = 3 # Adjust according to your dataset
dbscan_opt = DBSCAN(eps=eps, min_samples=min_samples)

# Fit DBSCAN to your data
dbscan_opt.fit(df)

# Extract cluster labels
cluster_labels = dbscan_opt.labels_
n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
colors = ['purple', 'red', 'blue', 'green', 'orange', 'yellow', 'brown', 'black', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'lime', 'teal', 'coral', 'lightblue', 'lightgreen', 'lavender', 'tan', 'salmon', 'gold', 'darkred', 'darkblue', 'darkgreen', 'darkorange', 'darkyellow', 'darkbrown', 'darkpink', 'darkgray', 'darkolive', 'darkcyan', 'darkmagenta', 'darklime', 'darkteal', 'darkcoral', 'darklightblue', 'darklightgreen', 'darklavender', 'darktan', 'darksalmon', 'darkgold']

fig = plt.figure(figsize = (10, 10))
ax = fig.add_subplot(projection='3d')

for i in range(len(cluster_labels)):
    if cluster_labels[i] == -1:  # Noise points
        ax.scatter(df[i][4], df[i][0], df[i][1], s=df[i][3], c='black', marker='x')
        
    else:
        ax.scatter(df[i][4], df[i][0], df[i][1], s=df[i][3], c=cluster_labels[i], cmap=matplotlib.colors.ListedColormap(colors[cluster_labels[i]]))

ax.set_xlabel('MAX freq (Hz)', fontsize=11)
ax.set_ylabel('Ampltude (m)', fontsize=11)
ax.set_zlabel('Energy (J)', fontsize=11)
ax.set_title(f'DBSCAN Clustering - {n_clusters} clusters found', fontsize=20)
plt.show()
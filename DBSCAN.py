from sklearn.cluster import DBSCAN 
from calculate_parameters import parameters
from matplotlib import pyplot as plt
import matplotlib
from sklearn.neighbors import NearestNeighbors
import numpy as np
from Data_filtering import filter_dataset

trai_start = 15000
trai_end = 16000

#plotting parameters
#indices: 0 amplitude, 1 energy, 2 rise time, 3 count, 4 max freq, 5 variance_e10
elev = 80 #elevation angle
azim = 0 #azimuthal angle (z-axis rotation)
xplot = 4
yplot = 0
zplot = 2
sizeplot = 5 #4th dimension corresponds to the size of the dot on the graph
plotting_variables = ['Amplitude', 'Energy', 'Rise time', 'Count', 'Frequency at max amplitude of FFT', 'Variance e10']

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

# Plotting the clusters
fig = plt.figure(figsize = (10, 10))
ax = fig.add_subplot(projection='3d')

for i in range(len(cluster_labels)):
    if cluster_labels[i] == -1:  # Noise points
        ax.scatter(df[i][xplot], df[i][yplot], df[i][zplot], s=df[i][sizeplot]/max(df[:,sizeplot])*40, c='black', marker='x')
        
    else:
        ax.scatter(df[i][xplot], df[i][yplot], df[i][zplot], s=df[i][sizeplot]/max(df[:,sizeplot])*40, c=cluster_labels[i], cmap=matplotlib.colors.ListedColormap(colors[cluster_labels[i]]))


ax.set_xlabel(plotting_variables[xplot], fontsize=11)
ax.set_ylabel(plotting_variables[yplot], fontsize=11)
ax.set_zlabel(plotting_variables[zplot], fontsize=11)
ax.set_title(f'DBSCAN Clustering - {n_clusters} clusters found', fontsize=20)
subtitle_text = f'Size of the dot corresponds to {plotting_variables[sizeplot]}'
ax.annotate(subtitle_text, (0.5, 1), xycoords='axes fraction', xytext=(0, -14), textcoords='offset points', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.view_init(elev, azim) 

plt.show()
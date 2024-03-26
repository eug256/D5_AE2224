from calculate_parameters import parameters
from numpy import unique
from numpy import where
from matplotlib import pyplot as plt
from sklearn.datasets import make_classification
from sklearn.cluster import DBSCAN
import time
import matplotlib

# Start timer
start_time = time.perf_counter()

# initialize the data set we'll work with
training_data=parameters(900,1500)
# define the model
amount_of_clusters = 7
minimum_samples_per_cluster = round(len(training_data)/amount_of_clusters/15)
dbscan_model = DBSCAN(eps=20, min_samples=minimum_samples_per_cluster)

# train the model
dbscan_model.fit(training_data)

# Extract cluster labels
cluster_labels = dbscan_model.labels_
colors = ['purple', 'red', 'blue', 'green','cyan','magenta','yellow','orange']

# assign each data point to a cluster
dbscan_result = dbscan_model.fit_predict(training_data)

# get all of the unique clusters
dbscan_cluster = unique(dbscan_result)

# plot the DBSCAN clusters
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for i in range(len(training_data)):
    ax.scatter(training_data[i][4], training_data[i][0],training_data[i][1], s=training_data[i][3] ,c=cluster_labels[i], cmap=matplotlib.colors.ListedColormap(colors[cluster_labels[i]]))

# End timer
end_time = time.perf_counter()

# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)

# show the DBSCAN plot
plt.show()
print(training_data.shape)
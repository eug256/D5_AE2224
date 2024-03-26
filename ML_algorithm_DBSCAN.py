from calculate_parameters import parameters
from numpy import unique
from numpy import where
from matplotlib import pyplot
from sklearn.datasets import make_classification
from sklearn.cluster import DBSCAN
import time

# Start timer
start_time = time.perf_counter()

# initialize the data set we'll work with
training_data=parameters(900,1000)
# define the model
dbscan_model = DBSCAN(eps=0.25, min_samples=4)

# train the model
dbscan_model.fit(training_data)

# assign each data point to a cluster
dbscan_result = dbscan_model.fit_predict(training_data)

# get all of the unique clusters
dbscan_cluster = unique(dbscan_result)

# plot the DBSCAN clusters
for dbscan_cluster in dbscan_cluster:
    # get data points that fall in this cluster
    index = where(dbscan_result == dbscan_cluster)
    # make the plot
    for i in index[0]:
        pyplot.scatter(training_data[i][5], training_data[i][6])

# End timer
end_time = time.perf_counter()

# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)

# show the DBSCAN plot
pyplot.show()
print(training_data.shape)
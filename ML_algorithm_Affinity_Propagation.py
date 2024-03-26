from calculate_parameters import parameters
from numpy import unique
from numpy import where
from matplotlib import pyplot
from sklearn.datasets import make_classification
<<<<<<< Updated upstream
from sklearn.cluster import AffinityPropagation
import time

# Start timer
start_time = time.perf_counter()
=======
from sklearn.cluster import AffinityPropagation, k_means
>>>>>>> Stashed changes

# initialize the data set we'll work with
training_data = parameters(2700,3000)
# define the model
model = AffinityPropagation(damping=0.7)

# train the model
model.fit(training_data)

# assign each data point to a cluster
result = model.predict(training_data)

# get all of the unique clusters
clusters = unique(result)

# plot the clusters
for cluster in clusters:
    # get data points that fall in this cluster
    index = where(result == cluster)
    # make the plot
    for i in index[0]:
<<<<<<< Updated upstream
        pyplot.scatter(training_data[i][1], training_data[i][5])

# End timer
end_time = time.perf_counter()

# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)
=======
        df=k_means.labels_

        # Plotting resulting clusters
        colors=['purple','red','blue','green']
        pyplot.scatter(training_data[i][4], training_data[i][0], c=df['KMeans_labels'],cmap=pyplot.colors.ListedColormap(colors))
>>>>>>> Stashed changes

# show the plot
pyplot.show()
print(training_data.shape)
from calculate_parameters import parameters
from numpy import unique
from numpy import where
from matplotlib import pyplot
from sklearn.datasets import make_classification
from sklearn.cluster import OPTICS

# initialize the data set we'll work with
training_data = parameters(1000)

# define the model
optics_model = OPTICS(eps=0.75, min_samples=1000)

# assign each data point to a cluster
optics_result = optics_model.fit_predict(training_data)

# get all of the unique clusters
optics_clusters = unique(optics_result)

# plot OPTICS the clusters
for optics_cluster in optics_clusters:
    # get data points that fall in this cluster
    index = where(optics_result == optics_clusters)
    print(index[0])
    # make the plot
    for i in index[0]:
        pyplot.scatter(training_data[i][4], training_data[i][0])

# show the OPTICS plot
pyplot.show()

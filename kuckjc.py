from sklearn.cluster import DBSCAN 
from calculate_parameters import parameters
from numpy import unique
from numpy import where
from matplotlib import pyplot as plt
import matplotlib

# Initialize the data set we'll work with
trai_start = 100
trai_end = 200
df = parameters(trai_start,trai_end)

# Initialize DBSCAN with desired parameters
dbscan_opt = DBSCAN(eps=50, min_samples=10)

# Fit DBSCAN to your data
dbscan_opt.fit(df)

# Extract cluster labels
cluster_labels = dbscan_opt.labels_
colors = ['purple', 'red', 'blue', 'green']

plt.figure(figsize=(10, 10))
for i in range(trai):
    plt.scatter(df[i][4], df[i][0], c=cluster_labels[i], cmap=matplotlib.colors.ListedColormap(colors[cluster_labels[i]]))

plt.title('DBSCAN Clustering', fontsize=20)
plt.xlabel('Feature 1', fontsize=14)
plt.ylabel('Feature 2', fontsize=14)
plt.show()

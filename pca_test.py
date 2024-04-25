import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
DATA = os.path.join(HERE, "1-10000-full.csv")

X = pd.read_csv(DATA) # read data
X_scaled = StandardScaler().fit(X).transform(X)

#define PCA model to use
pca = PCA(n_components=8)

#fit PCA model to data
pca_fit = pca.fit(X_scaled)
pca_transform = pca_fit.transform(X_scaled)

pca_fit_transform = pca.fit_transform(X_scaled)
df = pd.DataFrame(pca_fit_transform)
df2 = df.iloc[:, : 5]
df2.to_csv("1-10000-full-pca.csv",index=False)

PC_values = np.arange(pca.n_components_) + 1
plt.plot(PC_values, pca.explained_variance_ratio_, 'o-', linewidth=2, color='blue')
plt.title('Scree Plot')
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained')
plt.show()

print(pca.explained_variance_ratio_*100)
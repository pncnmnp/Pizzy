# libraries used : sklearn
from sklearn.neighbors import KNeighborsClassifier
from pandas import read_csv
import numpy as np

neigh = KNeighborsClassifier(n_neighbors=5, algorithm='auto')
# add your file address
df = read_csv('../../datasets/pizza_data.csv')
df = np.array(df)

neigh.fit(df[:, 0:3], df[:, 3])
# tests
print(neigh.predict([[1, 200, 50], [2, 1800, 100], [3, 750, 50]]))
# libraries used : sklearn,pandas,numpy
from sklearn.neighbors import KNeighborsClassifier
from pandas import read_csv
import numpy as np
from sklearn.model_selection import train_test_split
import pickle

def predict_user_priority(data):
		#data is a 2D list
		#create classifier

	#Remove Commment to Train the Alogrithm Again
	"""neigh = KNeighborsClassifier(n_neighbors=5, algorithm='auto')
	with open('Priority_decider.pickle','wb') as f:
		pickle.dump(neigh,f)
	"""

	pickle_in = open('Priority_decider.pickle','rb')
	neigh = pickle.load(pickle_in)
		# add your file address
	df = read_csv('pizza_data.csv')
		#define x and y Labels
	x = np.array(df.drop(['priority'],1))
	y = np.array(df['priority'])
		#shuffle the existing data
	x_train,x_test,y_train,y_test = train_test_split(x[1:],y[1:],test_size = 0.2)
		#fit the data 
	neigh.fit(x_train[1:],y_train[1:])
	ans = neigh.predict(data)
	ans = ans[0]
	return(ans)
	


# ans = predict_user_priority([[1,100,25]])
# print(ans)
# print(type(ans))

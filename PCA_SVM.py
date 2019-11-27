import h5py
import numpy as np
from random import seed
from random import random
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from datetime import datetime

if __name__ == "__main__":
	startTime = datetime.now()
 
 	# seed random number generator
	seed(7)

	num_gene = 19
	num_segments = 93877
	arrhythmia_num = 14
	print("*****Arrhythmia Number is:", arrhythmia_num, "*****")

	# import the training  data
	train_dataset = np.loadtxt("RESCALED_V3_PCA_Vectors_REDUCED.csv", delimiter=",")
	print("---> Loaded dataset")
#	train_dataset = np.loadtxt("V2_subset.csv", delimiter=",")
	
	# split data into training and testing datasets
	X = train_dataset[:,16:num_gene]
	#Y = train_dataset[:,0:16]
	Y = train_dataset[:,arrhythmia_num]
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=7)
	print("---> Split dataset")
	
	if arrhythmia_num == 0:
		gammas = [0.0001, 0.01, 1, 100, 10000]
		Cs = [0.0001, 0.01, 1, 100, 10000]
	elif arrhythmia_num == 1:
		gammas = [0.0001, 0.01, 1, 100, 10000]
		Cs = [0.0001, 0.01, 1, 100, 10000]
	elif arrhythmia_num == 1:
		gammas = [0.0001, 0.01, 1, 100, 10000]
		Cs = [0.0001, 0.01, 1, 100, 10000]
	elif arrhythmia_num == 1:
		gammas = [0.0001, 0.01, 1, 100, 10000]
		Cs = [0.0001, 0.01, 1, 100, 10000]
	elif arrhythmia_num == 1:
		gammas = [0.0001, 0.01, 1, 100, 10000]
		Cs = [0.0001, 0.01, 1, 100, 10000]
	else:
		gammas = [0.0001, 0.01, 1, 100, 10000]
		Cs = [0.0001, 0.01, 1, 100, 10000]
	
	param_grid = {'C': Cs, 'gamma' : gammas}

	#Create a svm Classifier
	#balanced_accuracy, f1_weighted
	clf = GridSearchCV(SVC(kernel='sigmoid',class_weight='balanced'),param_grid,scoring='balanced_accuracy',n_jobs=-1,verbose=1,return_train_score=True)
	# train the svm for fitness evaluation
	print("---> Created SVM (sigmoid)")
	clf.fit(X_train, Y_train)
	print("---> Trained SVM")
	Y_pred = clf.predict(X_test)
	print("Accuracy:",metrics.accuracy_score(Y_test, Y_pred))
	print("Balanced accuacy:",metrics.balanced_accuracy_score(Y_test, Y_pred))
	print("Precision:",metrics.precision_score(Y_test, Y_pred))
	print("Recall:",metrics.recall_score(Y_test, Y_pred))
	print("F1 score:",metrics.f1_score(Y_test,Y_pred))
	print("Weighted F1 score:",metrics.f1_score(Y_test,Y_pred,average='weighted'))
	print("Time taken:",(datetime.now() - startTime))
	print("Confusion matrix:",metrics.confusion_matrix(Y_test,Y_pred))
	print(clf.best_params_)	
	print("Gammas:",gammas)
	print("Cs:",Cs)
	print("*****Arrhythmia Number is:", arrhythmia_num, "*****")
	print("---------------------------------------------------------")
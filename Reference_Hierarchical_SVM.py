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
import sys
import re
import csv
import os

if __name__ == "__main__":
	startTime = datetime.now()
 
 	# seed random number generator
	seed(7)

	# import the training  data
	train_dataset = np.loadtxt("RESCALED_PCA_HIERARCHICAL_SVM.csv", delimiter=",")
	print("---> Loaded dataset")
	
	# split data into training and testing datasets
	X_orig = train_dataset[:,5:8]
	Y_orig = train_dataset[:,0:5]

	X_train_1st_stage, X_test_1st_stage, Y_train_1st_stage, Y_test_1st_stage = train_test_split(X_orig, Y_orig, test_size=0.3, random_state=7)
	print("---> Split dataset for 1st stage")

	gammas = [0.0001, 0.01, 1, 100, 10000]
	Cs = [0.0001, 0.01, 1, 100, 10000]

	gamma_1st_stage = 0.0001
	c_1st_stage = 10000
	
	param_grid = {'C': Cs, 'gamma' : gammas}

	#Create a svm Classifier
	clf_1st_stage = SVC(kernel='sigmoid',class_weight='balanced',gamma=gamma_1st_stage,C=c_1st_stage)
	#clf_1st_stage = GridSearchCV(SVC(kernel='sigmoid',class_weight='balanced'),param_grid,scoring='f1_weighted',n_jobs=-1,verbose=1,return_train_score=True)
	# train the svm for fitness evaluation
	print("---> Created SVM (sigmoid)")
	clf_1st_stage.fit(X_train_1st_stage, Y_train_1st_stage[:,4])
	print("---> Trained SVM")
	Y_pred_1st_stage = clf_1st_stage.predict(X_test_1st_stage)
	print("Accuracy:",metrics.accuracy_score(Y_test_1st_stage[:,4], Y_pred_1st_stage))
	print("Balanced accuacy:",metrics.balanced_accuracy_score(Y_test_1st_stage[:,4], Y_pred_1st_stage))
	print("Precision:",metrics.precision_score(Y_test_1st_stage[:,4], Y_pred_1st_stage))
	print("Recall:",metrics.recall_score(Y_test_1st_stage[:,4], Y_pred_1st_stage))
	print("F1 score:",metrics.f1_score(Y_test_1st_stage[:,4],Y_pred_1st_stage))
	print("Weighted F1 score:",metrics.f1_score(Y_test_1st_stage[:,4],Y_pred_1st_stage,average='weighted'))
	print("Time taken:",(datetime.now() - startTime))
	print("Confusion matrix:",metrics.confusion_matrix(Y_test_1st_stage[:,4],Y_pred_1st_stage))
	#print(clf_1st_stage.best_params_)	
	print("*****1st stage completed*****")
	print("---------------------------------------------------------")

	num_N_predicted = int(np.sum(Y_pred_1st_stage))

	N_data = np.zeros((num_N_predicted,4))
	S_data = np.zeros((num_N_predicted,4))
	V_data = np.zeros(((len(Y_pred_1st_stage)-num_N_predicted),4))
	F_data = np.zeros(((len(Y_pred_1st_stage)-num_N_predicted),4))
	
	index_1st = 0
	index_2nd = 0

	for index in range(0,len(Y_pred_1st_stage)):
		if Y_pred_1st_stage[index] == 1:
			N_data[index_1st,0] = Y_test_1st_stage[index,0]
			N_data[index_1st,1:4] = X_test_1st_stage[index,0:3]

			S_data[index_1st,0] = Y_test_1st_stage[index,1]
			S_data[index_1st,1:4] = X_test_1st_stage[index,0:3]

			index_1st = index_1st + 1
		else:
			V_data[index_2nd,0] = Y_test_1st_stage[index,2]
			V_data[index_2nd,1:4] = X_test_1st_stage[index,0:3]

			F_data[index_2nd,0] = Y_test_1st_stage[index,3]
			F_data[index_2nd,1:4] = X_test_1st_stage[index,0:3]
			
			index_2nd = index_2nd + 1

	X_N = N_data[:,1:4]
	Y_N = N_data[:,0]
	X_S = S_data[:,1:4]
	Y_S = S_data[:,0]
	X_V = V_data[:,1:4]
	Y_V = V_data[:,0]
	X_F = F_data[:,1:4]
	Y_F = F_data[:,0]

	X_train_N_stage, X_test_N_stage, Y_train_N_stage, Y_test_N_stage = train_test_split(X_N, Y_N, test_size=0.3, random_state=7)
	print("---> Split dataset for N stage")
	X_train_S_stage, X_test_S_stage, Y_train_S_stage, Y_test_S_stage = train_test_split(X_S, Y_S, test_size=0.3, random_state=7)
	print("---> Split dataset for S stage")
	X_train_V_stage, X_test_V_stage, Y_train_V_stage, Y_test_V_stage = train_test_split(X_V, Y_V, test_size=0.3, random_state=7)
	print("---> Split dataset for V stage")
	X_train_F_stage, X_test_F_stage, Y_train_F_stage, Y_test_F_stage = train_test_split(X_F, Y_F, test_size=0.3, random_state=7)
	print("---> Split dataset for F stage")

	#Create a svm Classifier
	clf_N_stage = GridSearchCV(SVC(kernel='sigmoid',class_weight='balanced'),param_grid,scoring='accuracy',n_jobs=-1,verbose=1,return_train_score=True)
	# train the svm for fitness evaluation
	print("---> Created N SVM (sigmoid)")
	clf_N_stage.fit(X_train_N_stage, Y_train_N_stage)
	print("---> Trained N SVM")
	Y_pred_N_stage = clf_N_stage.predict(X_test_N_stage)
	print("N Accuracy:",metrics.accuracy_score(Y_test_N_stage, Y_pred_N_stage))
	print("N Balanced accuacy:",metrics.balanced_accuracy_score(Y_test_N_stage, Y_pred_N_stage))
	print("N Precision:",metrics.precision_score(Y_test_N_stage, Y_pred_N_stage))
	print("N Recall:",metrics.recall_score(Y_test_N_stage, Y_pred_N_stage))
	print("N F1 score:",metrics.f1_score(Y_test_N_stage,Y_pred_N_stage))
	print("N Weighted F1 score:",metrics.f1_score(Y_test_N_stage,Y_pred_N_stage,average='weighted'))
	print("N Time taken:",(datetime.now() - startTime))
	print("N Confusion matrix:",metrics.confusion_matrix(Y_test_N_stage,Y_pred_N_stage))
	print(clf_N_stage.best_params_)	
	print("*****N stage completed*****")
	print("---------------------------------------------------------")

	#Create a svm Classifier
	clf_S_stage = GridSearchCV(SVC(kernel='sigmoid',class_weight='balanced'),param_grid,scoring='accuracy',n_jobs=-1,verbose=1,return_train_score=True)
	# train the svm for fitness evaluation
	print("---> Created S SVM (sigmoid)")
	clf_S_stage.fit(X_train_S_stage, Y_train_S_stage)
	print("---> Trained S SVM")
	Y_pred_S_stage = clf_S_stage.predict(X_test_S_stage)
	print("S Accuracy:",metrics.accuracy_score(Y_test_S_stage, Y_pred_S_stage))
	print("S Balanced accuacy:",metrics.balanced_accuracy_score(Y_test_S_stage, Y_pred_S_stage))
	print("S Precision:",metrics.precision_score(Y_test_S_stage, Y_pred_S_stage))
	print("S Recall:",metrics.recall_score(Y_test_S_stage, Y_pred_S_stage))
	print("S F1 score:",metrics.f1_score(Y_test_S_stage,Y_pred_S_stage))
	print("S Weighted F1 score:",metrics.f1_score(Y_test_S_stage,Y_pred_S_stage,average='weighted'))
	print("S Time taken:",(datetime.now() - startTime))
	print("S Confusion matrix:",metrics.confusion_matrix(Y_test_S_stage,Y_pred_S_stage))
	print(clf_S_stage.best_params_)	
	print("*****S stage completed*****")
	print("---------------------------------------------------------")

	#Create a svm Classifier
	clf_V_stage = GridSearchCV(SVC(kernel='sigmoid',class_weight='balanced'),param_grid,scoring='accuracy',n_jobs=-1,verbose=1,return_train_score=True)
	# train the svm for fitness evaluation
	print("---> Created V SVM (sigmoid)")
	clf_V_stage.fit(X_train_V_stage, Y_train_V_stage)
	print("---> Trained V SVM")
	Y_pred_V_stage = clf_V_stage.predict(X_test_V_stage)
	print("V Accuracy:",metrics.accuracy_score(Y_test_V_stage, Y_pred_V_stage))
	print("V Balanced accuacy:",metrics.balanced_accuracy_score(Y_test_V_stage, Y_pred_V_stage))
	print("V Precision:",metrics.precision_score(Y_test_V_stage, Y_pred_V_stage))
	print("V Recall:",metrics.recall_score(Y_test_V_stage, Y_pred_V_stage))
	print("V F1 score:",metrics.f1_score(Y_test_V_stage,Y_pred_V_stage))
	print("V Weighted F1 score:",metrics.f1_score(Y_test_V_stage,Y_pred_V_stage,average='weighted'))
	print("V Time taken:",(datetime.now() - startTime))
	print("V Confusion matrix:",metrics.confusion_matrix(Y_test_V_stage,Y_pred_V_stage))
	print(clf_V_stage.best_params_)	
	print("*****V stage completed*****")
	print("---------------------------------------------------------")

	#Create a svm Classifier
	clf_F_stage = GridSearchCV(SVC(kernel='sigmoid',class_weight='balanced'),param_grid,scoring='accuracy',n_jobs=-1,verbose=1,return_train_score=True)
	# train the svm for fitness evaluation
	print("---> Created F SVM (sigmoid)")
	clf_F_stage.fit(X_train_F_stage, Y_train_F_stage)
	print("---> Trained F SVM")
	Y_pred_F_stage = clf_F_stage.predict(X_test_F_stage)
	print("F Accuracy:",metrics.accuracy_score(Y_test_F_stage, Y_pred_F_stage))
	print("F Balanced accuacy:",metrics.balanced_accuracy_score(Y_test_F_stage, Y_pred_F_stage))
	print("F Precision:",metrics.precision_score(Y_test_F_stage, Y_pred_F_stage))
	print("F Recall:",metrics.recall_score(Y_test_F_stage, Y_pred_F_stage))
	print("F F1 score:",metrics.f1_score(Y_test_F_stage,Y_pred_F_stage))
	print("F Weighted F1 score:",metrics.f1_score(Y_test_F_stage,Y_pred_F_stage,average='weighted'))
	print("F Time taken:",(datetime.now() - startTime))
	print("F Confusion matrix:",metrics.confusion_matrix(Y_test_F_stage,Y_pred_F_stage))
	print(clf_F_stage.best_params_)	
	print("*****F stage completed*****")
	print("---------------------------------------------------------")
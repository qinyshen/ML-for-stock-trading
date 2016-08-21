import numpy as np
import json
from sklearn.svm import SVC, LinearSVC
from sklearn.cross_validation import StratifiedKFold
from sklearn import metrics
from string import punctuation
import string
import os
import pymysql.cursors
import glob
from numpy import *
import matplotlib.pyplot as plt

def performance(y_true, y_pred, metric="accuracy"):
    """
        Calculates the performance metric based on the agreement between the
        true labels and the predicted labels
        Input:
          y_true- (n,) array containing known labels
          y_pred- (n,) array containing predicted scores
          metric- string option used to select the performance measure
        Returns: the performance as a np.float64
    """
    if metric == "accuracy":
      performance_score = metrics.accuracy_score(y_true, y_pred)

    elif metric == "f1-score":
      performance_score = metrics.f1_score(y_true, y_pred)

    elif metric == "auroc":
      performance_score = metrics.roc_auc_score(y_true, y_pred)

    elif metric == "precision":
      performance_score = metrics.precision_score(y_true, y_pred)

    elif metric == "sensitivity":
      matrix = metrics.confusion_matrix(y_true, y_pred, [1,-1])
      TP = matrix[0][0]
      FN = matrix[0][1]
      FP = matrix[1][0]
      TN = matrix[1][1]
      performance_score = (TP)*1.0/(TP+FN)
      
    elif metric == "specificity":
      matrix = metrics.confusion_matrix(y_true, y_pred, [1,-1])
      TP = matrix[0][0]
      FN = matrix[0][1]
      FP = matrix[1][0]
      TN = matrix[1][1]

      performance_score = (TN)*1.0/(TN+FP)
    #print "score"
    #print np.float64(performance_score)
    return np.float64(performance_score)




def cv_performance(clf, X, y, k=5, metric="accuracy"):
    """
        Splits the data, X and y, into k-folds and runs k-fold crossvalidation:
        training a classifier on K-1 folds and testing on the remaining fold.
        Calculates the k-fold crossvalidation performance metric for classifier
        clf by averaging the performance across folds.
        Input:
          clf- an instance of SVC()
          X- (n,d) array of feature vectors, where n is the number of examples
             and d is the number of features
          y- (n,) array of binary labels {1,-1}
          k- int specificyin the number of folds (default=5)
          metric- string specifying the performance metric (default='accuracy',
                   other options: 'f1-score', 'auroc', 'precision', 'sensitivity',
                   and 'specificity')
        Returns: average 'test' performance across the k folds as np.float64
    """
    skf = StratifiedKFold(y, k)
    times = 0
    added = 0

    for train_index, test_index in skf:
      X_train, X_test = X[train_index], X[test_index]
      y_train, y_test = y[train_index], y[test_index]
      clf.fit(X_train, y_train)
      dic = clf.decision_function(X_test)
      for i, item in enumerate (dic):
        if item > 0:
          dic[i] = 1;
        else:
          dic[i] = -1; 
      performance_score = performance(y_test, dic, metric)
      #print performance_score
      added += np.float64(performance_score)
      times += 1

    avg_performance_score = 1.0*added/times

    return np.float64(avg_performance_score)



def select_param_quadratic(X, y, k=5, metric="accuracy", C_range=[]):
    # Sweeps different settings for the hyperparameters of an quadratic-kernel SVM,
    # calculating the k-fold CV performance for each setting on X, y.
    # Input:
    #   X- (n,d) array of feature vectors, where n is the number of examples
    #      and d is the number of features
    #   y- (n,) array of binary labels {1,-1}
    #   k- int specificyin the number of folds (default=5)
    #   metric- string specifying the performance metric (default='accuracy',
    #            other options: 'f1-score', 'auroc', 'precision', 'sensitivity',
    #            and 'specificity')
    # Returns the parameter value(s) for an quadratic-kernel SVM, that 'maximize'
    # the average 5-fold CV performance.
	bestC = 0
	bestR = 0
	best_score = 0

	for c in C_range:
	  for r in C_range:
	    clf = SVC(kernel='poly', degree=2, C=c, coef0=r)
	    #print c
	    score = cv_performance(clf, X, y, k, metric)
	    #print score
	    #print c
	    #print r

	    if score > best_score:
	      best_score = score
	      bestC = c
	      bestR = r

	print metric
	print "----------------------"
	print best_score
	print bestC 
	print bestR 

	return bestR, bestC





def my_performance(clf, X, y, metric="accuracy"):
    dic = clf.decision_function(X)
    for i, item in enumerate (dic):
      if item > 0:
        dic[i] = 1;
      else:
        dic[i] = -1; 
    performance_score = performance(y, dic, metric)
    return np.float64(performance_score)


def performance_CI(clf, X, y, metric="accuracy"):
    """
        Estimates the performance of clf on X,y and the corresponding 95%CI
        (lower and upper bounds)
        Input:
          clf-an instance of SVC() that has already been fit to data
          X- (n,d) array of feature vectors, where n is the number of examples
             and d is the number of features
          y- (n,) array of binary labels {1,-1}
          metric- string specifying the performance metric (default='accuracy',
                   other options: 'f1-score', 'auroc', 'precision', 'sensitivity',
                   and 'specificity')
        Returns:
            a tuple containing the performance of clf on X,y and the corresponding
            confidence interval (all three values as np.float64's)
    """
    score = my_performance(clf, X, y, metric)
    tmp = []
    for num in range(1000): 
      X_tmp = []
      y_tmp = []
      for i in range(len(y)): 
        sample = np.random.choice(len(y), replace=True)
        X_tmp.append(X[sample])
        y_tmp.append(y[sample])

      rate = my_performance(clf, X_tmp, y_tmp, metric)
      tmp.append(rate)

    tmp = sorted(tmp)
    lower = tmp[24]
    upper = tmp[974]

    return score, lower, upper
    #return score








def show_money(symbol, money):
    cursor = connection.cursor()
    cursor.execute("select count(*) from $%s;" % symbol)
    connection.commit()
    results = cursor.fetchall()
    minutes = range(results[0][0] - 1)
    plt.figure(1)
    plt.plot(minutes, money, label='Money', color='orange')
    cursor.execute("select open from $%s;" % symbol)
    connection.commit()
    results = cursor.fetchall()
    rate = float(1000 / results[0][0])
    price = [i[0] * rate for i in results[:-1]]
    plt.plot(minutes, price, label='Index', color='green')
    # plt.plot(minutes, index, label='Stocks', color='blue')

    plt.xlabel('Time(minutes)')
    plt.ylabel('Price(dollars)')
    plt.title(symbol)
    plt.show()

def extract_feature_vectors(database_name):
    #a feature matrix of dimension (number of each stock times minutes, number of feature)
	connection = pymysql.connect(user='root', password='root', database=database_name)
	fr = open('aim_stock.txt')
	index_list = [index_info.strip().split(' ')[0] for index_info in fr.readlines()]
	cursor = connection.cursor()

	feature_matrix =[]

	result_price = []

	binary_result = []

	for index in index_list:
		commit = "select * from $%s;" % index
		cursor.execute(commit)
		results = cursor.fetchall()
		m = len(results)


		for i in range(5, m - 1):
				Open = results[i - 5][2]
				High = max([each[3] for each in results[i - 5:i]])
				Low = min([each[4] for each in results[i - 5:i]])
				Close = results[i][5]
				Volume = float(sum([each[6] for each in results[i - 5:i]])) / 100
				Label = results[i + 1][5]
				dataSet = [Open, High, Low, Close, Volume]

				feature_matrix.append(dataSet)
				result_price.append(Open)

		#last day dont have result
		result_price = result_price[1:]
		feature_matrix.pop()

	for feature, result in zip(feature_matrix, result_price):
		if (result * (1 - 0.0000184) - 0.005) > feature[3]:
			binary_result.append(1)
		else:	
			binary_result.append(-1)

	return feature_matrix, np.array(binary_result)







# feature_matrix, result_price =  extract_feature_vectors("tickets")
feature_matrix, result_price = extract_feature_vectors("tickets")

total = len(result_price)
training_total = int(total*3/4)

print str(total)
print str(training_total)


X = np.split(feature_matrix, [training_total, total])
y = np.split(result_price,[training_total, total])


clf = SVC(kernel = 'poly', degree = 2, C = 0.01, coef0 = 10000)
clf.fit(X[0], y[0])

print performance_CI(clf, X[1], y[1], "accuracy")


# metric = ["accuracy", "f1-score", "auroc", "precision", "sensitivity", "specificity"]

# bestC = [0.01, 0.01, 0.01, 10000, 0.0001, 1]
# bestR = [10000, 10000, 10000, 0.1, 0.0001, 1000]

# C_range = [0.0001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
# linear = [0.1, 0.1, 0.1, 0.1, 0.0001 ,1]

# linear_Kernel = [100, 100, 1000, 0.1, 1000, 0.0001]

# bestC_5 = [0.1, 0.1, 0.1, 10, 0.0001, 1]
# bestR_5 = [1000, 1000, 1000, 100, 0.0001, 10000]


# linear_Kernel_5 = [1000, 0.1, 100, 10000, 0.1, 0.0001]




# def part_3():
#   select_param_linear(X[0], y[0], 5, "accuracy", C_range)
#   select_param_linear(X[0], y[0], 5, "f1-score", C_range)
#   select_param_linear(X[0], y[0], 5, "auroc", C_range)
#   select_param_linear(X[0], y[0], 5, "precision", C_range)
#   select_param_linear(X[0], y[0], 5, "sensitivity", C_range)
#   select_param_linear(X[0], y[0], 5, "specificity", C_range)

#   select_param_quadratic(X[0], y[0], 5, "accuracy", C_range)
#   select_param_quadratic(X[0], y[0], 5, "f1-score", C_range)
#   select_param_quadratic(X[0], y[0], 5, "auroc", C_range)
#   select_param_quadratic(X[0], y[0], 5, "precision", C_range)
#   select_param_quadratic(X[0], y[0], 5, "sensitivity", C_range)
#   select_param_quadratic(X[0], y[0], 5, "specificity", C_range)


# for i in range(len(metric)):
#   clf = SVC(kernel = 'linear', C=linear[i])
#   clf.fit(X[0], y[0])
#   print metric[i]
#   print performance_CI(clf, X[1], y[1], metric=metric[i])


# for i in range(len(metric)):
#   clf = LinearSVC(penalty='l1', dual=False, C=linear_Kernel[i])
#   clf.fit(X[0], y[0])
#   print metric[i]
#   print performance_CI(clf, X[1], y[1], metric=metric[i])






















import os
import pymysql.cursors
import glob
from numpy import *
import matplotlib.pyplot as plt

connection = pymysql.connect(user='root', password='root',
                             database='tickets')
fr = open('aim_stock.txt')
index_list = [index_info.strip().split(' ')[0] for index_info in fr.readlines()]
cursor = connection.cursor()
weights = ones(4)
numIter = 100
count = 0


def store_weights(input, file_name):
    import pickle
    fw = open(file_name, 'w')
    pickle.dump(input, fw)
    fw.close()


for index in index_list:
    commit = "select * from $%s;" % index
    cursor.execute(commit)
    results = cursor.fetchall()
    m = len(results)
    for j in range(numIter):
        list = range(m-1)[5:]
        random.shuffle(list)
        for i in list:
            Open = results[i-5][2]
            High = max([each[3] for each in results[i-5:i]])
            Low = min([each[4] for each in results[i-5:i]])
            Close = results[i][5]
            Volume = float(sum([each[6] for each in results[i-5:i]])) / 100
            Label =results[i+1][5]
            dataSet = array([Open, High, Low, Close])
            # print Open, High, Low, Close, Volume
            alpha = 4 / (1.0 + j + i) / 10000000 + 0.000001
            h = sum(dataSet * weights)
            error = Label - h
            # print error
            weights += alpha * error * dataSet
    count += 1

store_weights(weights, 'weights.txt')
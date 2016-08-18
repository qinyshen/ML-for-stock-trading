import os
import pymysql.cursors
import glob
from numpy import *

connection = pymysql.connect(user='root', password='root',
                             database='tickets')
fr = open('aim_stock.txt')
index_list = [index_info.strip().split(' ')[0] for index_info in fr.readlines()]
cursor = connection.cursor()
weights = ones(4)
numIter = 100
count = 0
'''
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
            alpha = 4 / (1.0 + j + i ) / 10000000 + 0.000001
            h = sum(dataSet * weights)
            error = Label - h
            # print error
            weights += alpha * error * dataSet
    count += 1
'''
# print weights
# weights = array(weights)
weights = array([0.24061739, 0.24743389, 0.25011055, 0.26169569])
money1 = 0

for index in index_list:
    error_count = 0
    miss = 0
    money = 1000.0
    rest = 1000.0
    index_num1 = 0
    index_num2 = 0
    commit = "select * from $%s;" % index
    cursor.execute(commit)
    results = cursor.fetchall()
    m = len(results)
    move = 0
    price = 0
    error = 0
    for i in range(5, m - 1):
        # prediction
        Open = results[i - 5][2]
        High = max([each[3] for each in results[i - 5:i]])
        Low = min([each[4] for each in results[i - 5:i]])
        Close = results[i][5]
        Volume = float(sum([each[6] for each in results[i - 5:i]])) / 100
        Label = results[i + 1][5]
        dataSet = array([Open, High, Low, Close])
        h = sum(dataSet * weights)
        error = error + (Label - h) / Label
        if (h - Open) * (Label - Open) < 0:
            error_count += 1
        if (Label - h) / Label > 0.0001:
            miss += 1
        # trade
        if index_num1 > 0:
            if Close * (1 - 0.0000184) > price:
                rest += index_num1 * Close * (1 - 0.0000184)
                index_num1 = 0
        if index_num2 > 0:
            rest -= index_num2 * Close
            index_num2 = 0
        if h - Close > 0:
            if index_num1 == 0:
                move = 1
                index_num1 += int(rest * 1 / results[i + 1][2])
                rest -= index_num1 * results[i + 1][2]
                price = results[i + 1][2]
        '''
        elif h - Close < 0:
            if index_num2 == 0:
                move = 2
                index_num2 += int(rest * 1 / High)
                rest += index_num2 * results[i+1][2]
        '''

        money = rest + index_num1 * results[i + 1][2] - index_num2 * results[i + 1][2]
        '''
        print "************ %d ************" % i
        print h, Close, Label
        print move
        print index_num1, index_num2
        print money, rest
        '''
    print "************ %s ************" % index
    money1 += money
    print money
    print float(error_count) / (m - 5)
    print float(error) / (m - 5)
    print float(miss) / (m - 5)

print "*****************************"
print float(money1 / 33000)

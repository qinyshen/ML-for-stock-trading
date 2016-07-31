import os
import pymysql.cursors
import glob
from numpy import *


connection = pymysql.connect(user='root', password='root',
                             database='tickets')
fr = open('aim_stock.txt')
index_list= [index_info.strip().split(' ')[0] for index_info in fr.readlines()]
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
        list = range(m-1)
        random.shuffle(list)
        for i in list:
            Open = results[i][2]
            High = results[i][3]
            Low = results[i][4]
            Close = results[i][5]
            Volume = float(results[i][6]) / 100
            Label =results[i+1][2]
            dataSet = array([Open, High, Low, Close])
            # print Open, High, Low, Close, Volume
            alpha = 4 / (1.0 + j + i ) / 10000000 + 0.000001
            h = sum(dataSet * weights)
            error = Label - h
            # print error
            weights += alpha * error * dataSet
    count += 1
'''
weights = array([0.2518305, 0.24969401, 0.25011781, 0.24829426])
for index in index_list[:1]:
    error_count = 0
    money = 1000.0
    rest = 1000.0
    index_num = 0
    commit = "select * from $%s;" % index
    cursor.execute(commit)
    results = cursor.fetchall()
    m = len(results)
    move = 0
    for i in range(m-1):
        Open = results[i][2]
        High = results[i][3]
        Low = results[i][4]
        Close = results[i][5]
        Volume = float(results[i][6]) / 100
        Label =results[i+1][2]
        dataSet = array([Open, High, Low, Close])
        h = sum(dataSet * weights)
        error = Label - h
        if (h - Open) * (Label -Open) < 0:
            error_count += 1
        if h - Open > 0:
            if index_num > 0:
                move = -1
                index_num -= int(index_num * 0.4)
                rest += int(index_num * 0.4) * Label
        elif h - Open < 0:
            if index_num >= 0:
                move = 1
                index_num += int(rest * 0.4 / Label)
                rest -= int(rest * 0.4 / Label) * Label
        money = rest + index_num * Label
        print h, Open, rest, index_num, Label, move, money
    print float(error_count)/(m-1)
    print money
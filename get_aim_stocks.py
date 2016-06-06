import re
import sys
import math
import os
import glob
from collections import defaultdict
import pymysql.cursors
import csv


def store_index_list(input_set, file_name):
    fw = open(file_name, 'w')
    fw.writelines(input_set)
    fw.close()

connection = pymysql.connect(user='root', password='root',
                             database='tickets')
cursor = connection.cursor()
commit = "select * from Prepared ORDER BY AMV"
cursor.execute(commit)
results = cursor.fetchall()
length = len(results)
aim_stock = []

# here to get the membership in the last 300 of SP500 as aim_stock
sp500 = open('sp500.txt', 'r')
symbols = []
for item in sp500:
    symbol = item.split(",")[0]
    symbols.append(symbol)

last300 = symbols[-300:]

for stock in results[int(length * 0.34): int(length * 0.67)]:
    if 30 >= stock[1] >= 10 and 30 >= stock[2] >= 10:
        each_stock = []
        each_stock.extend([stock[0] + ' ' + str(stock[1]) + ' ' + str(stock[2]) + ' ' + str(stock[3]) + '\n'])
        if stock[0] in last300:
            print "OK"
            aim_stock.extend(each_stock)

store_index_list(aim_stock, 'aim_stock.txt')
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
cursor.execute(
    "create table IF NOT EXISTS Prepared(symbol varchar(20) NOT NULL, max DOUBLE, min DOUBLE, AMV DOUBLE, PRIMARY KEY(symbol));")
connection.commit()

cursor.execute("SHOW TABLES")
indexes = cursor.fetchall()
index_list = []


print indexes

for each_index in indexes:
    if each_index[0] == 'Prepared':
        continue
    commit = "select count(*) from Prepared where symbol = %s"
    cursor.execute(commit, each_index[0])
    count = cursor.fetchall()[0][0]
    cursor.execute("select max(open) from %s" % each_index[0])
    max = cursor.fetchall()[0][0]
    cursor.execute("select min(open) from %s" % each_index[0])
    min = cursor.fetchall()[0][0]
    cursor.execute("select AVG(volume) from %s" % each_index[0])
    AMV = cursor.fetchall()[0][0]
    if count == 0:
        sql = "INSERT INTO `Prepared` (`symbol`, `max`, `min`, `AMV`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (each_index[0].split('$')[1], max, min, AMV))
        connection.commit()
    index_list.extend([each_index[0].split('$')[1] + ' ' + str(max) + ' ' + str(min) + ' ' + str(AMV) + '\n'])
store_index_list(index_list, 'index_list.txt')

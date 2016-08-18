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
                             database='mydb')
cursor = connection.cursor()
cursor.execute("select distinct symbol from Ticket")
indexes = cursor.fetchall()
index_list = []
for each_index in indexes:
    print each_index[0]
    cursor = connection.cursor()
    cursor.execute("select max(open) from Ticket where symbol = %s",each_index[0])
    max = cursor.fetchall()[0][0]
    cursor.execute("select min(open) from Ticket where symbol = %s", each_index[0])
    min = cursor.fetchall()[0][0]
    cursor.execute("select AVG(volume) from Ticket where symbol = %s", each_index[0])
    AMV = cursor.fetchall()[0][0]
    sql = "INSERT INTO `Prepared` (`symbol`, `max`, `min`, `AMV`) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (each_index[0], max, min, AMV))
    connection.commit()
    index_list.extend([each_index[0] + ' ' + str(max) + ' ' + str(min) + ' ' + str(AMV)])
print index_list
store_index_list(index_list,'index_list.txt')


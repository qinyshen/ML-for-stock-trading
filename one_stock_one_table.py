import re
import sys
import math
import os
import glob
from collections import defaultdict
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(user='root', password='root',
                             database='tickets')

# open file and break
path = "DATA/"
count = 0

for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(filename, 'r') as sub_infile:
        tmp = filename.split("/")[1]
        symbol = tmp.split(".")[0]
        cursor = connection.cursor()
        commit = "CREATE TABLE IF NOT EXISTS $%s (date DATE,time TIME, Open DOUBLE,High DOUBLE,Low DOUBLE,Close DOUBLE,Volume int);" % symbol
        print commit
        cursor.execute(commit)
        connection.commit()
        # print symbol
        commit = "select count(*) from $%s;" % symbol
        cursor.execute(commit)
        count = cursor.fetchall()[0][0]
        if count == 0:
            for sub_line in sub_infile:
                # print sub_line
                sub_items = sub_line.split()
                date = sub_items[0]
                time = sub_items[1]
                Open = sub_items[2]
                High = sub_items[3]
                Low = sub_items[4]
                Close = sub_items[5]
                Volume = sub_items[6]
                # write into db

                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO $%s " % symbol
                    sql = sql + "(date, time, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (date, time, Open, High, Low, Close, Volume))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
                # connection.close()
        else:
            print 'gone'
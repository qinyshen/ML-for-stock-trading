import re
import sys
import math
import os
import glob
from collections import defaultdict
import pymysql.cursors
import csv

# Connect to the database
connection = pymysql.connect(user='root', password='root',
                             database='mydb')
cursor = connection.cursor()
cursor.execute("select distinct symbol from Ticket")
indexes = cursor.fetchall()
indexlist = []
for each_index in indexes[0:1]:
    print each_index
    cursor = connection.cursor()
    cursor.execute("select max(open) from Ticket where symbol = %s",each_index)
    max = cursor.fetchall()[0]
    cursor.execute("select min(open) from Ticket where symbol = %s", each_index)
    min = cursor.fetchall()[0]
    cursor.execute("select AVG(volume) from Ticket where symbol = %s", each_index)
    ADV = cursor.fetchall()[0]
    print str(max) + ' ' + str(min) + ' ' + str(ADV)



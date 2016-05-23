import re
import sys
import math
import os
import glob
from collections import defaultdict
import pymysql.cursors
# Connect to the database
connection = pymysql.connect(user='root', password='root',
                             database='mydb')

cursor = connection.cursor()
cursor.execute("select symbol,date,time,Count(*) from Ticket Group By symbol,time,date Having Count(*)>1;")
results = cursor.fetchall()
print results
count = 0
for data in results:
    with connection.cursor() as cursor:
        count += 1
        print 'delete '+str(count)+' time : ' + str(data[3]-1) + 'row(s)'
        commit = "DELETE FROM Ticket WHERE symbol=%s and date=%s and time=%s LIMIT %s;"
        cursor.execute(commit, (data[0], data[1], data[2], data[3]-1))
    connection.commit()


import re
import sys
import math
import os
import glob
from collections import defaultdict
import pymysql.cursors
# Connect to the database
connection = pymysql.connect(user='root', password='root',
                             database='learnMySQL')
cursor = connection.cursor()
name = ['x','xx']
number = ['11', '12']
for i in range(2):
    sql = "INSERT INTO `room` (`name`,`number`) VALUES (%s, %s)"
    cursor.execute(sql, (name[i], number[i]))
    connection.commit()

cursor = connection.cursor()
cursor.execute("select * from room")
results = cursor.fetchall()
print results
name =[]
number = []
for data in results:
    name.append(data[0])
    number.append(data[1])
name = tuple(name)
number =tuple(number)
print name
print number
commit = "DELETE FROM room WHERE name in ('x','xx') and number LIMIT 1;"
cursor.execute(commit)
connection.commit()

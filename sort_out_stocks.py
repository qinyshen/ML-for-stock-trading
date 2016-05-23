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
cursor.execute("select * from room")
results = cursor.fetchall()
for re in results:
    print re
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


#open file and break
path = "test/"
for filename in glob.glob(os.path.join(path, '*.txt')):			
	with open(filename, 'r') as sub_infile:
		tmp = filename.split("/")[1]
		symbol = tmp.split(".")[0]
		# print symbol
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
			#write into db
			
			with connection.cursor() as cursor:
			# Create a new record
				sql = "INSERT INTO `Ticket` (`symbol`, `date`, `time`, `Open`, `High`, `Low`,`Close`, `Volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, (symbol, date, time, Open, High, Low, Close, Volume))

			# connection is not autocommit by default. So you must commit to save
			# your changes.
			connection.commit()
	# connection.close()

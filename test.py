import re
import sys
import math
import os
import glob
from collections import defaultdict
import pymysql.cursors
import csv

sp500 = open('sp500.txt', 'r')
symbols = []
for item in sp500:
	symbol = item.split(",")[0]
	symbols.append(symbol)

last300 = symbols[-300:]	
#now reomve not in it
if 'WU' in last300:
	print "here"


#print last300
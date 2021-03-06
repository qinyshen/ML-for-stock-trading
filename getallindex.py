import google
import csv
import os


def get_all_index(break_pt=""):
    index_list1 = csv.reader(file('data/NASDAQ.csv', 'rb'))
    index_list2 = csv.reader(file('data/NYSE.csv', 'rb'))

    table1 = [line for line in index_list1]
    table2 = [line for line in index_list2]
    rows1 = len(table1)
    rows2 = len(table2)
    indexes = [0] * (rows1 + rows2 - 2)
    for i in range(rows1 - 1):
        indexes[i] = table1[i + 1][0]
    for i in range(rows2 - 1):
        indexes[i + rows1 - 1] = table2[i + 1][0]
    if not os.path.exists('DATA'):
        os.makedirs('DATA')
    start = False
    for each_index in indexes:
        if not break_pt:
            start = True
        if not start and each_index == break_pt:
            start = True
        if start:
            google.get_google_finance_intraday(each_index)

get_all_index("MTD")


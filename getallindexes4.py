from googlefinance import get_google_finance_intraday
import csv
import os
import thread
import time


def get_indexes(indexes, root, finished_thread):
    for each_index in indexes:
        sign = get_google_finance_intraday(each_index, root)
        print each_index + ' : ' + sign
    finished_thread[0] += 1


def get_all_index():
    index_list1 = csv.reader(file('1.csv', 'rb'))
    index_list2 = csv.reader(file('2.csv', 'rb'))
    table1 = [line for line in index_list1]
    table2 = [line for line in index_list2]
    indexes1 = [init[0] for init in table1[1:]]
    indexes2 = [init[0] for init in table2[1:]]
    m1 = len(indexes1)/2
    m2 = len(indexes2)/2
    finished_thread = [0]
    root = 'DATA1/'
    if not os.path.exists(root):
        os.makedirs(root)
    try:
        thread.start_new_thread(get_indexes, (indexes1[m1:], root, finished_thread))
        thread.start_new_thread(get_indexes, (indexes1[:m1], root, finished_thread))
        thread.start_new_thread(get_indexes, (indexes2[m2:], root, finished_thread))
        thread.start_new_thread(get_indexes, (indexes2[:m2], root, finished_thread))
    except:
        print "Error: unable to start thread"
    while finished_thread[0] < 4:
        time.sleep(10)
        pass


get_all_index()

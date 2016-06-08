from googlefinance import get_google_finance_intraday
import csv
import os
import thread
import time


def get_indexes(indexes, root, finished_thread):
    process = '-1'
    flag = 1
    while not process == indexes[-1]:
        for each_index in indexes:
            if each_index == process:
                flag = 1
            if flag == 1:
                try:
                    sign = get_google_finance_intraday(each_index, root)
                    print each_index + ' : ' + sign
                    process = each_index
                except:
                    process = each_index
                    flag = 0
                    break
    finished_thread[0] += 1


def get_all_index():
    index_list1 = csv.reader(file('1.csv', 'rb'))
    index_list2 = csv.reader(file('2.csv', 'rb'))
    table1 = [line for line in index_list1]
    table2 = [line for line in index_list2]
    indexes1 = [init[0] for init in table1[1:]]
    indexes2 = [init[0] for init in table2[1:]]
    m1 = len(indexes1) / 2
    m2 = len(indexes2) / 2
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

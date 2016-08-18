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
    fr = open('aim_stock.txt')
    indexes1 = [index_info.strip().split(' ')[0] for index_info in fr.readlines()]
    m1 = len(indexes1) / 2
    finished_thread = [0]
    root = 'DATA1/'
    if not os.path.exists(root):
        os.makedirs(root)
    try:
        thread.start_new_thread(get_indexes, (indexes1[m1:], root, finished_thread))
        thread.start_new_thread(get_indexes, (indexes1[:m1], root, finished_thread))
    except:
        print "Error: unable to start thread"
    while finished_thread[0] < 2:
        time.sleep(10)
        pass


get_all_index()

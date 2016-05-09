import google
import os


def get_all_index():
    index_list = open('NYSE.txt')
    indexs = [inst for inst in index_list.readlines()]
    print indexs
    for eachindex in indexs:
        google.get_google_finance_intraday(eachindex)

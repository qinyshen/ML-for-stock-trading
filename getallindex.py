from google import get_google_finance_intraday


def get_all_index():
    index_list = open('NYSE.txt')
    print index_list
    indexes = [inst.strip().split('\r') for inst in index_list.readlines()]
    for each_index in indexes:
        get_google_finance_intraday(each_index)


get_all_index()
import google

def get_all_index():
    index_list = open('NYSE.txt')
    print index_list
    indexs = [inst.strip().split('\r') for inst in index_list.readlines()]
    print indexs
    for eachindex in indexs:
        print eachindex
        google.get_google_finance_intraday(eachindex)


get_all_index()
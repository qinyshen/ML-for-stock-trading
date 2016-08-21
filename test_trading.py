import os
import pymysql.cursors
import glob
from numpy import *
import matplotlib.pyplot as plt

connection = pymysql.connect(user='root', password='root',
                             database='tickets')
fr = open('aim_stock.txt')
index_list = [index_info.strip().split(' ')[0] for index_info in fr.readlines()]
cursor = connection.cursor()

def show_money(symbol, money):
    cursor = connection.cursor()
    cursor.execute("select count(*) from $%s;" % symbol)
    connection.commit()
    results = cursor.fetchall()
    minutes = range(results[0][0] - 1)
    plt.figure(1)
    plt.plot(minutes, money, label='Money', color='orange')
    cursor.execute("select open from $%s;" % symbol)
    connection.commit()
    results = cursor.fetchall()
    rate = float(1000 / results[0][0])
    price = [i[0] * rate for i in results[:-1]]
    plt.plot(minutes, price, label='Index', color='green')
    # plt.plot(minutes, index, label='Stocks', color='blue')

    plt.xlabel('Time(minutes)')
    plt.ylabel('Price(dollars)')
    plt.title(symbol)
    plt.show()



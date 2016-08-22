import pymysql.cursors
from numpy import *
import matplotlib.pyplot as plt
from sklearn.externals import joblib

connection = pymysql.connect(user='root', password='root',
                             database='tickets')
fr = open('aim_stock1.txt')
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


money1 = 0
num = 32

for index in index_list[:num]:
    clf = joblib.load('model/%s/clf.model' % index)
    error_count = 0
    hold = 0
    money = 1000.0
    rest = 1000.0
    tax = 0
    commission = 0
    index_num1 = 0
    index_num2 = 0
    commit = "select * from $%s;" % index
    cursor.execute(commit)
    results = cursor.fetchall()
    m = len(results)
    price = 0
    trade_times = 0
    time = 0
    index_history = [0, 0, 0, 0, 0]
    money_history = [1000, 1000, 1000, 1000, 1000, ]
    for i in range(5, m - 1):
        # prediction
        Open = results[i - 5][2]
        High = max([each[3] for each in results[i - 5:i]])
        Low = min([each[4] for each in results[i - 5:i]])
        Close = results[i][5]
        Volume = float(sum([each[6] for each in results[i - 5:i]])) / 100
        Label = results[i + 1][5]
        dataSet = array([Open, High, Low, Close, Volume]).reshape(1, -1)
        prediction = clf.predict(dataSet)
        # trade
        if index_num1 > 0:
            if Close * (1 - 0.0000184) > (price + 0.01) or (i - time) >= 40:  # 0.0000184 is trading tax
                rest += index_num1 * Close * (1 - 0.0000184) - index_num1 * 0.005
                commission += index_num1 * 0.01
                tax += index_num1 * Close * 0.0000184
                index_num1 = 0
                trade_times += 1
                hold += i - time
        if prediction * (Label - results[i + 1][2]) < 0:
            error_count += 1
        if prediction > 0:
            if index_num1 == 0 :
                move = 1
                index_num1 += int(rest * 1 / results[i + 1][2])
                rest -= index_num1 * results[i + 1][2] + index_num1 * 0.005
                price = results[i + 1][2]
                time = i

        money = rest + index_num1 * results[i + 1][2]
        money_history.append(money)
        index_history.append(index_num1)
        '''
        print "************ %d ************" % i
        print h, Close, Label
        print move
        print index_num1, index_num2
        print money, rest
        '''
    money1 += money

    print "************ %s ************" % index
    print "money : %f" % money
    print "trade : %d" % trade_times
    # print "hold : %d" % (hold / trade_times)
    print "tax : %f" % tax
    print "commission : %f" % commission
    print "up-down error : %f" % (float(error_count) / (m - 5))
    # show_money(index, money_history)

print "*****************************"
print float(money1 / (num * 1000))

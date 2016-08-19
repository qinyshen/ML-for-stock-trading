import pymysql.cursors
from numpy import *
import matplotlib.pyplot as plt

connection = pymysql.connect(user='root', password='root',
                             database='tickets')
fr = open('aim_stock1.txt')
index_list = [index_info.strip().split(' ')[0] for index_info in fr.readlines()]
cursor = connection.cursor()


def load_weights(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)


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


# print weights
weights = load_weights('weights.txt')
print weights
# weights = array([0.24061739, 0.24743389, 0.25011055, 0.26169569])
money1 = 0

for index in index_list:
    error_count = 0
    hold = 0
    miss = 0
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
    error = 0
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
        dataSet = array([Open, High, Low, Close])
        h = sum(dataSet * weights)
        error = error + abs((Label - h) / Label)
        if (h - results[i + 1][2]) * (Label - results[i + 1][2]) < 0:
            error_count += 1
        if abs((Label - h) / Label) > 0.0001:
            miss += 1
        # trade
        if index_num1 > 0:
            if Close * (1 - 0.0000184) > (price + 0.01) or (i - time) >= 40:  # 0.0000184 is trading tax
                rest += index_num1 * Close * (1 - 0.0000184) - index_num1 * 0.005
                commission += index_num1 * 0.01
                tax += index_num1 * Close * 0.0000184
                index_num1 = 0
                trade_times += 1
                hold += i - time
        if index_num2 > 0:
            rest -= index_num2 * Close
            index_num2 = 0
        if h - Close > 0:
            if index_num1 == 0 and h > Close + 0.01:
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
    print "hold : %d" % (hold / trade_times)
    print "tax : %f" % tax
    print "commission : %f" % commission
    print "up-down error : %f" % (float(error_count) / (m - 5))
    print "precision : %f" % (float(error) / (m - 5))
    print "miss more than 0.0001 : %f " % (float(miss) / (m - 5))
    # show_money(index, money_history)

print "*****************************"
print float(money1 / 32000)

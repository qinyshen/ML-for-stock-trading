import matplotlib.pyplot as plt
import pymysql.cursors

connection = pymysql.connect(user='root', password='root',
                             database='tickets')


def show_index(symbol):
    cursor = connection.cursor()
    cursor.execute("select time,open from $%s;" % symbol)
    connection.commit()
    results = cursor.fetchall()

    price = [i[1] for i in results]

    plt.figure(1)
    plt.plot(price, marker='')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(symbol)
    plt.show()

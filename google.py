#!/usr/bin/env python 
"""
Retrieve intraday stock data from Google Finance.
"""

import csv
import datetime
import re

import pandas as pd
from pandas import DataFrame
import requests


def get_google_finance_intraday(ticker, period=60, days=15):
    """
    Retrieve intraday stock data from Google Finance.
    Parameters
    ----------
    ticker : str
        Company ticker symbol.
    period : int
        Interval between stock values in seconds.
    days : int
        Number of days of data to retrieve.
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """

    uri = 'http://www.google.com/finance/getprices' \
          '?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'.format(ticker=ticker,
                                                                          period=period,
                                                                          days=days)
    requests.adapters.DEFAULT_RETRIES = 3
    s = requests.session()
    s.keep_alive = False
    # page = requests.get(uri, proxies={"http": "127.0.0.1:9743"})
    page = requests.get(uri)
    reader = csv.reader(page.content.splitlines())
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    rows = []
    times = []
    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=period*int(row[0])))
            rows.append(map(float, row[1:]))

    if len(rows):
        PD = DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'), columns=columns)
        deal_data(PD, times, ticker)
        # return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),
        #                     columns=columns)
    else:
        return DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))


def deal_data(PD, times, ticker):
    stock_data = []
    for date in times:
        each_data = []
        each_data.extend([date.strftime("%Y-%m-%d %H:%M:%S") + ' ' + PD['Open'][date].__str__() + ' ' + PD['High'][
            date].__str__() + ' ' + PD['Low'][date].__str__() + ' ' + PD['Close'][date].__str__() + ' ' + PD['Volume'][
                              date].__str__() + '\n'])
        stock_data.extend(each_data)
    store_stock_data(stock_data, ticker + '.txt')


def store_stock_data(data_set, filename):
    fw = open(filename, 'w')
    fw.writelines(data_set)
    fw.close()


get_google_finance_intraday("AAPL")
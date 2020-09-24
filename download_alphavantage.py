#from alpha_vantage.timeseries import TimeSeries
import yfinance as yf
import sqlite3

#ts = TimeSeries(key='GSEF5CJ9Q8B2IS0P', output_format='pandas')


import time
secs = 15

conn = sqlite3.connect('db.sqlite3')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('select * from instvol_stock')
sql_results = c.fetchall()
for row in sql_results:
    print(row['ticker'])
    try:
        symbol = yf.Ticker(row['ticker'])
        print(symbol.history(period="max").head())
#        data, meta_data = ts.get_daily_adjusted(symbol=row['ticker'], outputsize='full')
#        print(data.head())
    except:
        print('No such a ticker.')
    
    print('\n')

#    print('SPX')
#    data, meta_data = ts.get_daily_adjusted(symbol='SPX', outputsize='full')
#    print(data.head())

    time.sleep(secs)

conn.close()

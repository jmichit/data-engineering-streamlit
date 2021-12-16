
from sqlite3 import connect, Error
import datetime
import pandas as pd
import requests

class StockDB2():
    
    def __init__(self, filepath):
        try: 
            self.conn = connect(filepath)
            self.cursor = self.conn.cursor()
            print('Database connected.' + str(datetime.datetime.now()))
            
        except Error as e:
            return e
    
#     def __del__(self):
        
#         if self.conn:
#             try:
#                 self.cursor.close()
#                 self.conn.close()
#                 print('Database has been closed.' + str(datetime.datetime.now()))
#             except Exception as e:
#                 print(f'Error: {e}')
#         else:
#             print("Database already closed")
            
    def close(self):
        if self.conn:
            try:
                self.conn.close()
                print('Database closed' + str(datetime.datetime.now()))
            except Exception as e:
                print(f'Error: {e}')
        else:
            print("Database already closed")
    
    def delete_ticker(self, ticker):
        sql = "delete from prices where ticker = ?"
        args = (ticker,)
        self.cursor.execute(sql, args)
        self.conn.commit()

    def clear_db(self):
        sql = "delete from prices"
        self.cursor.execute(sql)
        self.conn.commit()

    def db_summary(self):
        # sql = """
        # select ticker, count(*), max(close), min(close),
        #        avg(close), min(date), max(date)
        # from prices
        # group by ticker
        # order by 1
        # """
        # self.cursor.execute(sql)
        # x = self.cursor.fetchall()
        # columns = ['Ticker', 'Rows', 'Max Price', 'Min Price',
        #            'Avg Price', 'Min Date', 'Max Date']
        #return x, columns           

        url = 'https://g324209f0c2c559-db202112160000.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/api/dbinfo'

        # params = {'function':'TIME_SERIES_DAILY',
        #           'symbol': ticker,
        #           'outputsize' : outputsize,    
        #           'apikey': self.apikey}

        # response = requests.get(url, params=params)
        response = requests.get(url, params=params)

        data  = response.json()

        # fname = 'compact-' + ticker + '.pkl'
        # with open(fname, 'wb') as file:
        #     pkl.dump(data, file )

        dailyprices = data['items']

        #We are using the daily close price    
        # prices = [(x, float(dailyprices[x]['4. close'])) for x in dailyprices.keys()]

        return pd.DataFrame(dailyprices).sort_index()
        # return pd.DataFrame(x, columns=columns).set_index('Ticker')

    def get_stock_prices(self, ticker):
        sql = """
        select date, close
        from prices
        where ticker = ?
        order by date
        """
        args= (ticker,)
        self.cursor.execute(sql, args)
        x = self.cursor.fetchall()

        columns = ['Date', 'Price']
        return pd.DataFrame(x, columns = columns) 

    def get_stock_prices_date_range(self, ticker, start_date, end_date):
        sql = """
        select date, close
        from prices
        where ticker = ?
        and date between ? and ?
        order by date
        """
        args= (ticker, start_date, end_date)
        self.cursor.execute(sql, args)
        x = self.cursor.fetchall()

        columns = ['Date', 'Price']
        return pd.DataFrame(x, columns = columns) 

    def entries(self, ticker, startdate, enddate):
        sql = """
        with temp as (
            select ticker, 
                   date,
                   close,
                   min(close) over(partition by ticker 
                                   order by date
                                   rows between 
                                   9 preceding and
                                   current row) as S1min,
                   max(close) over(partition by ticker 
                                   order by date 
                                   rows between 
                                   19 preceding and
                                   current row) as S1max
            from prices
            where ticker = ?
            and date between ? and ?
        )

        select ticker,
               date,
               close, 
               S1min, 
               S1max,
               case when close = S1min then "Exit"
                    when close = S1max then "Enter"
                    else ''
               end as signal
        from temp
        """
        args = (ticker, startdate, enddate)
        self.cursor.execute(sql, args)
        x = self.cursor.fetchall()
        columns = ['Ticker', 'Date', 'Close', 
                   '10 day Min Price', '20 day Max Price', 'Signal']
        return pd.DataFrame(x, columns=columns)
    
    def insert_daily_data(self, ticker, data):
        sql = "insert into prices (ticker, date, close) values (?, ?, ?)"

        for i, item in enumerate(data):
            args = (ticker, item[0], item[1])
            self.cursor.execute(sql, args)

        print(f"Row added:{i}")

        self.conn.commit()

        
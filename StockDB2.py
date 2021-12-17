import datetime
import pandas as pd
import requests

import streamlit as st

class StockDB2():
    """ 
    Class container for REST API calls to Oracle Autonomous Data Warehouse on the Cloud 
    """

    def db_summary(self):

        url = 'https://g324209f0c2c559-db202112160000.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/api/dbinfo'
        
        response = requests.get(url) 

        data  = response.json()

        dailyprices = data['items']

        print('Using REST API')

        temp = pd.DataFrame(dailyprices).set_index('ticker').sort_index()

        return temp

    def get_stock_prices_date_range(self, ticker, start_date, end_date):

        url = "https://g324209f0c2c559-db202112160000.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/api/get_daily_prices/{}/{}/{}"

        startdate = start_date.strftime('%Y-%m-%d')
        enddate = end_date.strftime('%Y-%m-%d')

        urlstr = url.format(ticker, startdate, enddate)

        print(urlstr)
        response = requests.get(urlstr)

        json = response.json()

        alldata = json['items']
        print(alldata)

        while json['hasMore']:
            for link in json['links']:
                if link['rel'] == 'next':
                    url_more = link['href']
                    break
            res = requests.get(url_more)
            json = res.json()
            data = json['items']    
            alldata.extend(data)

        temp = pd.DataFrame(alldata)
        temp.columns = ['Date', 'Price']

        return temp

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

        url = 'https://g324209f0c2c559-db202112160000.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/api/insert/{}/{}/{}'

        placeholder2 = st.empty()
        for i, item in enumerate(data):

            placeholder2.progress(i)

            urlstr = url.format(ticker, item[0], item[1])
            response = requests.post(urlstr) 
            print(response.status_code)

        return i + 1

    def add_indicator(self, indicator, days):

        url = 'https://g324209f0c2c559-db202112160000.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/api/indicator/{}/{}'

     
        urlstr = url.format(indicator, days)
        response = requests.post(urlstr) 
        print(response.status_code)

    def get_indicators(self):

        url = 'https://g324209f0c2c559-db202112160000.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/api/indicatorlist'

        response = requests.get(url) 
        
        data = response.json()

        indicators = data['items']

        temp = pd.DataFrame(dailyprices).set_index('name').sort_index()

        temp.columns = ['Name', '?day MA']

        return temp


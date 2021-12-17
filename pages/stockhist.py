import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import pandas as pd
import datetime

from StockDB import StockDB 
from StockDB2 import StockDB2 

from Accounts import Account

def app():
    col1, col2 = st.columns([2,2])

    # datemin = datetime.date(2000,1,4)
    # datemax = datetime.date(2021,12,1)


    # ticker = col1.text_input("Ticker", value='MSFT')

    # db = StockDB('stocks.db')

    db2 = StockDB2()
    stockinfo = db2.db_summary()
   
    #db.close()

    available_tickers = list(stockinfo.index)

    ticker =  col1.selectbox('Ticker', available_tickers)

    # datemin = datetime.date(pd.to_datetime(stockinfo.loc[ticker, 'Min Date']).year,
    #                         pd.to_datetime(stockinfo.loc[ticker, 'Min Date']).month,
    #                         pd.to_datetime(stockinfo.loc[ticker, 'Min Date']).day)

    # datemax = datetime.date(pd.to_datetime(stockinfo.loc[ticker, 'Max Date']).year,
    #                         pd.to_datetime(stockinfo.loc[ticker, 'Max Date']).month,
    #                         pd.to_datetime(stockinfo.loc[ticker, 'Max Date']).day)


    datemin = datetime.date(pd.to_datetime(stockinfo.loc[ticker, 'mindate']).year,
                            pd.to_datetime(stockinfo.loc[ticker, 'mindate']).month,
                            pd.to_datetime(stockinfo.loc[ticker, 'mindate']).day)

    datemax = datetime.date(pd.to_datetime(stockinfo.loc[ticker, 'maxdate']).year,
                            pd.to_datetime(stockinfo.loc[ticker, 'maxdate']).month,
                            pd.to_datetime(stockinfo.loc[ticker, 'maxdate']).day)

    defaultmin = max(datemin, datetime.date(2021, 10, 1))
    defaultmax = min(datemax, datetime.date(2021, 10, 31))
    
    #defaultmin = datetime.date(2021, 10, 1)
    #defaultmax = datetime.date(2021, 10, 31)


    startdate = col1.date_input('Start Date', min_value=datemin, max_value=datemax, value=defaultmin) 
    col1.text(f"Earliest Date: {datemin}")

    enddate = col1.date_input('End Date', min_value=datemin, max_value=datemax, value=defaultmax) 
    col1.text(f"Latest Date: {datemax}")

    balance = col1.text_input("Balance", value= 10000)

    fig, axis = plt.subplots()

    # db = StockDB("stocks.db")
    # df = db.get_stock_prices_date_range(ticker, startdate, enddate)
    df = db2.get_stock_prices_date_range(ticker, startdate, enddate)
    # db.close()

    #st.dataframe(df)


    account = Account(balance)

    #df.set_index('Date')

    def Buy_and_hold(df):
        """ 
        Purchase on the first day, sell on the last
        """
        df2 = df.copy()
        df2['Action'] = ''
        df2.loc[df2['Date'] == df2['Date'].min(), 'Action'] = 'Buy'
        df2.loc[df2['Date'] == df2['Date'].max(), 'Action'] = 'Sell'
        return df2

    def transactions(account, df):
        df['Account Value'] = -1
        df['Positions'] = ""

        for i, row in df.iterrows():
            if row['Action'] == 'Buy':
                account.maxpurchase(ticker, row['Price'])
            elif row['Action'] == 'Sell':
                account.sellall(ticker, row['Price'])   
            else:
                #No change to account
                pass
            row['Account Value'] = account.mktval({ticker:row['Price']})
            row['Position'] = account.list_positions()

        return df
    
        # df['Action'] = ''
        # df.iloc[0,2] = 'Buy'
        # df.iloc[-1,2] = 'Sell'
        # currprice = int(df.iloc[0,1])
        # print(currprice)

        # account.maxpurchase(ticker, currprice)
        # for i, row in df.iterrows():
        # #tickervals = {ticker : curprice}
        #     df['Acct Value'] =  df['Price'].apply(lambda x: account.mktval({ticker: x}))

    
    #    # df['Cash'] = -999
    #    # currprice = 64  #df.loc[startdate]['Price']

    #     account.maxpurchase(34, ticker)

    #     print(account.list_positions())
    # #    curprice = df['Price']
    #  #   tickervals = {ticker : curprice}
        
    #   #  df['Cash'] = account.cash.quantity
    #   #  df['MktValue'] = account.currvalue(tickervals)
        
    #     for i, row in df.iterrows():
    #         curprice = row['Price']
    #         tickervals = {ticker : curprice}
    #         row['Cash'] = account.cash.quantity
    #         print(account.cash.quantity)
    #         row['MktValue'] = account.mktval(tickervals)

    #     account.sellall(ticker, curprice)
    
    #    return df



    #signals = db.entries(ticker, startdate, enddate)

    sns.lineplot(x='Date', y='Price', data=df, ax=axis, label='Price')
    # sns.lineplot(x='Date', y='Price', data=df, label='Price')

    # sns.lineplot(x='Date', y='10 day Min Price', linestyle = "--", data=signals, ax=axis, label ='10 Day Min Price')

    # sns.lineplot(x='Date',y='20 day Max Price',  linestyle = '--', data=signals, ax=axis, label= '20 Day Max Price')

    #axis.legend(['price', '10 day Min' , '20 day Max'])
    axis.legend()



    # signals_summary = signals[signals['Signal'].isin(['Enter', 'Exit'])]

    #if df['Date'].size() > 30:

    indicies = np.linspace(0, df['Date'].size, dtype=int, num=30,  endpoint=False)
    axis.set_xticks(indicies)
    axis.set_xticklabels(df.iloc[indicies]['Date'],rotation=90)

    # plt.xticks(indicies)
    # plt.xlabel(df.iloc[indicies]['Date'],rotation=90)

    signals = Buy_and_hold(df)

    signals = transactions(account, signals)

    # signals = df.copy()
    # signals['Action'] = ''
    
    #when to buy
    buysignals = signals[signals['Action']=='Buy']
    if len(buysignals) > 0:
        sns.scatterplot(x='Date', y='Price', marker=10, data=buysignals, ax=axis, palette=['green'], label='Entries' )

    #when to sell
    sellsignals = signals[signals['Action']=='Sell']
    if len(sellsignals) > 0:
        sns.scatterplot(x='Date', y='Price', marker=11, data=sellsignals, ax=axis, palette=['red'], label='Exits' )

    #st.text("Strategy: Buy & Hold")

    st.pyplot(fig)

    st.table(signals)

    #p_and_l = float(signals.iloc[-1,3]) - float(signals.iloc[0,3])

    #st.text(f"Buy and Hold P&L ${round(p_and_l,2)}")

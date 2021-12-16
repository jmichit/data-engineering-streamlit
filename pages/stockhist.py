import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import pandas as pd
import datetime

from StockDB import StockDB 
from Accounts import Account

def app():
    col1, col2 = st.columns([1,3])

    # datemin = datetime.date(2000,1,4)
    # datemax = datetime.date(2021,12,1)


    # ticker = col1.text_input("Ticker", value='MSFT')

    db = StockDB('stocks.db')
    stockinfo = db.db_summary()
    db.close()

    available_tickers = list(stockinfo.index)

    ticker =  col1.selectbox('Ticker', available_tickers)

    datemin = datetime.date(pd.to_datetime(stockinfo.loc[ticker, 'Min Date']).year,
                            pd.to_datetime(stockinfo.loc[ticker, 'Min Date']).month,
                            pd.to_datetime(stockinfo.loc[ticker, 'Min Date']).day)

    datemax = datetime.date(pd.to_datetime(stockinfo.loc[ticker, 'Max Date']).year,
                            pd.to_datetime(stockinfo.loc[ticker, 'Max Date']).month,
                            pd.to_datetime(stockinfo.loc[ticker, 'Max Date']).day)


    startdate = col1.date_input('Start Date', min_value=datemin, max_value=datemax, value=datetime.date(2021,1,1)) 
    enddate = col1.date_input('End Date', min_value=datemin, max_value=datemax, value=datetime.date(2021, 1, 31)) 

    balance = col1.text_input("Balance", value= 10000)


    fig, axis = plt.subplots()

    db = StockDB("stocks.db")
    df = db.get_stock_prices_date_range(ticker, startdate, enddate)
    db.close()

    account = Account(balance)

    #df.set_index('Date')

    def Buy_and_hold(df):
        df['Action'] = ''
        df.iloc[0,2] = 'Buy'
        df.iloc[-1,2] = 'Sell'
        currprice = int(df.iloc[0,1])
        print(currprice)

        account.maxpurchase(ticker, currprice)
        for i, row in df.iterrows():
        #tickervals = {ticker : curprice}
            df['Acct Value'] =  df['Price'].apply(lambda x: account.mktval({ticker: x}))

    
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
    
        return df



    #signals = db.entries(ticker, startdate, enddate)

    sns.lineplot(x='Date', y='Price', data=df, ax=axis, label='Price')

    # sns.lineplot(x='Date', y='10 day Min Price', linestyle = "--", data=signals, ax=axis, label ='10 Day Min Price')

    # sns.lineplot(x='Date',y='20 day Max Price',  linestyle = '--', data=signals, ax=axis, label= '20 Day Max Price')

    #axis.legend(['price', '10 day Min' , '20 day Max'])
    axis.legend()



    # signals_summary = signals[signals['Signal'].isin(['Enter', 'Exit'])]

    #if df['Date'].size() > 30:
    indicies = np.linspace(0, df['Date'].size, dtype=int, num=30,  endpoint=False)
    axis.set_xticks(indicies)
    axis.set_xticklabels(df.iloc[indicies]['Date'],rotation=90)

    signals = Buy_and_hold(df)

    #when to buy
    buysignals = signals[signals['Action']=='Buy']
    sns.scatterplot(x='Date', y='Price', marker=10, data=buysignals, ax=axis, palette=['green'], label='Entries' )

    #when to sell
    sellsignals = signals[signals['Action']=='Sell']
    sns.scatterplot(x='Date', y='Price', marker=11, data=sellsignals, ax=axis, palette=['red'], label='Exits' )

    st.text("Strategy: Buy & Hold")

    st.pyplot(fig)



    st.table(signals)

    p_and_l = float(signals.iloc[-1,3]) - float(signals.iloc[0,3])

    st.text(f"Buy and Hold P&L ${round(p_and_l,2)}")

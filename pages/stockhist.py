import streamlit as st

from prophet import Prophet

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import pandas as pd
import datetime

from StockDB2 import StockDB2 
from Accounts import Account


def app():
    col1, col2 = st.columns([2,2])

    db2 = StockDB2()
    stockinfo = db2.db_summary()
   
    available_tickers = list(stockinfo.index)

    ticker =  col1.selectbox('Ticker', available_tickers)

    datemin = datetime.date(pd.to_datetime(stockinfo.loc[ticker, 'mindate']).year,
                            pd.to_datetime(stockinfo.loc[ticker, 'mindate']).month,
                            pd.to_datetime(stockinfo.loc[ticker, 'mindate']).day)

    datemax = datetime.date(pd.to_datetime(stockinfo.loc[ticker, 'maxdate']).year,
                            pd.to_datetime(stockinfo.loc[ticker, 'maxdate']).month,
                            pd.to_datetime(stockinfo.loc[ticker, 'maxdate']).day)

    defaultmin = max(datemin, datetime.date(2021, 10, 1))
    defaultmax = min(datemax, datetime.date(2021, 10, 31))
    
    startdate = col1.date_input('Start Date', min_value=datemin, max_value=datemax, value=defaultmin) 
    col1.text(f"Earliest Date: {datemin}")

    enddate = col1.date_input('End Date', min_value=datemin, max_value=datemax, value=defaultmax) 
    col1.text(f"Latest Date: {datemax}")

    balance = col1.text_input("Balance", value= 10000)

    fig, axis = plt.subplots()

    df = db2.get_stock_prices_date_range(ticker, startdate, enddate)


    ########

    def get_prophet_forecast(ticker, startdate, enddate, days):
        """
        Create a Prophet forecast based on `days` provided
        """

        p1 = Prophet()
        
        #find startdate for forecast
        forecast_startdate = startdate - datetime.timedelta(days=days)

        prior = db2.get_stock_prices_date_range(ticker, forecast_startdate, startdate)
        prior.columns = ['ds', 'y']
        prior['ds'] = pd.to_datetime(prior['ds'])
        p1.fit(prior)
        num_periods = (enddate - startdate + datetime.timedelta(days=1)).days
        future = p1.make_future_dataframe(periods=num_periods, include_history=False )
        forecast = p1.predict(future)
        forecast = forecast.rename(columns = {'ds':'Date', 'yhat':'Price'})
        return forecast

    forecast1 = get_prophet_forecast(ticker, startdate, enddate, 100)
    forecast2 = get_prophet_forecast(ticker, startdate, enddate, 200)


    # p1 = Prophet()

    # #forecast length = 200 days
    # forecast_startdate = startdate - datetime.timedelta(days=200)

    # prior = db2.get_stock_prices_date_range(ticker, forecast_startdate, startdate)
    # prior.columns = ['ds', 'y']
    # prior['ds'] = pd.to_datetime(prior['ds'])
    # p1.fit(prior)
    # num_periods = (enddate - startdate + datetime.timedelta(days=1)).days
    # future = p1.make_future_dataframe(periods=num_periods, include_history=False )
    # forecast1 = p1.predict(future)
    # forecast1 = forecast1.rename(columns = {'ds':'Date', 'yhat':'Price'})

    # #forecast length = 30 days
    # forecast_startdate = startdate - datetime.timedelta(days=30)

    # prior = db2.get_stock_prices_date_range(ticker, forecast_startdate, startdate)
    # prior.columns = ['ds', 'y']
    # prior['ds'] = pd.to_datetime(prior['ds'])
    # p1.fit(prior)
    # num_periods = (enddate - startdate + datetime.timedelta(days=1)).days
    # future = p1.make_future_dataframe(periods=num_periods, include_history=False )
    # forecast2 = p1.predict(future)
    # forecast2 = forecast2.rename(columns = {'ds':'Date', 'yhat':'Price'})



    #######

    # st.text('forecast')
    # st.table(forecast)

    # st.text('prices')
    # st.table(df)
   


    df = db2.get_stock_prices_date_range(ticker, startdate, enddate)

    account = Account(balance)

    #convert date string into date and sort
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)

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
        df['Account Value'] = account.cash
        df['Position'] = ""

        for i, row in df.iterrows():
            if row['Action'] == 'Buy':
                account.maxpurchase(ticker, row['Price'])
            elif row['Action'] == 'Sell':
                account.sellall(ticker, row['Price'])   
            else:
                #No change to account
                pass

            df.at[i, 'Account Value'] = account.mktval({ticker:row['Price']})
            df.at[i, 'Position'] = account.list_positions()

        return df

    #signals = db.entries(ticker, startdate, enddate)

    sns.lineplot(x='Date', y='Price', data=df, ax=axis, label='Price')
    sns.lineplot(x='Date', y='Price', data=forecast1, ax=axis, label='Forecast - 30 Days')
    sns.lineplot(x='Date', y='Price', data=forecast2, ax=axis, label='Forecast - 200 Days')
    
    axis.legend()

    indicies = np.linspace(0, df['Date'].size, dtype=int, num=30,  endpoint=False)
    axis.set_xticks(indicies)
    axis.set_xticklabels(df.iloc[indicies]['Date'],rotation=90)

    #apply default buy at start, sell at end strategy    
    signals = Buy_and_hold(df)

    #take buy / sell signals and adjust account
    signals = transactions(account, signals)
   
    #when to buy
    buysignals = signals[signals['Action']=='Buy']
    if len(buysignals) > 0:
        sns.scatterplot(x='Date', y='Price', marker=10, data=buysignals, ax=axis, palette=['green'], label='Entries' )

    #when to sell
    sellsignals = signals[signals['Action']=='Sell']
    if len(sellsignals) > 0:
        sns.scatterplot(x='Date', y='Price', marker=11, data=sellsignals, ax=axis, palette=['red'], label='Exits' )

    st.text("Strategy: Buy & Hold")

    st.pyplot(fig)


    st.table(signals)

    p_and_l = float(signals.iloc[-1,3]) - float(signals.iloc[0,3])

    st.text(f"Buy and Hold P&L ${round(p_and_l,2)}")

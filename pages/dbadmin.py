import streamlit as st

import pandas as pd

from StockDB2 import StockDB2 
from StockAPI import StocksAPI

def fetch_and_load_daily(db, api, ticker, outputsize="compact"):
    temp = api.get_daily_series(ticker, outputsize)
    rows = db.insert_daily_data(ticker, temp)
    return rows

def app():

    db2 = StockDB2()

    table = db2.db_summary()
    indicators = db2.get_indicators()

    available_tickers = list(table.index)

    placeholder1 = st.empty()
    placeholder1.subheader('Securities')    
    placeholder1.table(table)

    placeholder2 = st.empty()
    placeholder2.subheader('Indicators')
    placeholder2.table(indicators)

    col1, col2 = st.columns([2,2])

    #ADD Security form and action 
    col1.write("Add Security:")
    form1 = col1.form(key="addsecurity")
    with form1:
        ticker = st.text_input("Add Ticker:")
        actionAdd = st.form_submit_button(label="LOAD")
        st.write('WARNING: This could take a while.')

    if actionAdd:
        sa = StocksAPI()

        num = fetch_and_load_daily(db2, sa, ticker ) # outputsize='full')

        table = db2.db_summary()
        placeholder1.table(table)

        st.success(f"{num} rows loaded.")
        st.balloons()
        
        
    #DELETE Security form and action 
    col2.write('Delete Security:')
    form2 = col2.form(key="deletesecurity")
    with form2:
        ticker = st.selectbox('Remove Ticker', available_tickers)
        actionDelete = st.form_submit_button(label="REMOVE")

    if actionDelete:
        db2.delete_ticker(ticker) 

        st.success(f"{ticker} deleted.")
        st.balloons()
            
        table = db2.db_summary()

        placeholder1.table(table)


    #ADD indicator form and action
    st.write('Add Indicator') 
    form3 = st.form(key="addSMA")
    with form3:
        indicator = st.text_input("indicator")
        days = st.text_input("# days")

        actionAddIndicator = st.form_submit_button(label="CALC")
        st.write('WARNING: This could take a while.')

    if actionAddIndicator:
        sa = StocksAPI()
        db2.add_indicator(indicator, days)

        st.success(f"{indicator} created.")
        st.balloons()

        indicators = db2.get_indicators()
        
        placeholder2.table(indicators)
            
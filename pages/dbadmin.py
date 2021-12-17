import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import pandas as pd
import datetime


from StockDB2 import StockDB2 
#from StockDB import StockDB 
from StockAPI import StocksAPI
from Accounts import Account

def fetch_and_load_daily(db, api, ticker, outputsize="compact"):
    temp = api.get_daily_series(ticker, outputsize)
    rows = db.insert_daily_data(ticker, temp)
    return rows

def app():

    st.title('DBAdmin')

    #db = StockDB('stocks.db')
    
    db2 = StockDB2()

    table = db2.db_summary()
    available_tickers = list(table.index)

    #db.close()

    placeholder = st.empty()
    placeholder.table(table)

    col1, col2 = st.columns([2,2])


    col1.write("Add:")

    #ADD Security form and action 
    form1 = col1.form(key="addsecurity")
    with form1:
        ticker = st.text_input("Add Ticker:")
        # bug_type = cols[1].selectbox(
        #     "Bug type:", ["Front-end", "Back-end", "Data related", "404"], index=2
        # )
        # comment = st.text_area("Comment:")
        # cols = st.columns(2)
        # date = cols[0].date_input("Bug date occurrence:")
        # bug_severity = cols[1].slider("Bug severity:", 1, 5, 2)
        actionAdd = st.form_submit_button(label="LOAD")
        st.write('WARNING: This could take awhile.')

    if actionAdd:
        #db = StockDB('stocks.db')
        sa = StocksAPI()

        num = fetch_and_load_daily(db2, sa, ticker ) # outputsize='full')

        # db.close()

        table = db2.db_summary()
        placeholder.table(table)

        st.success(f"{num} rows loaded.")
        st.balloons()
        
        # db = StockDB('stocks.db'
        # db.close()
        
    #DELETE Security form and action 
    
    col2.write('Delete:')
    form2 = col2.form(key="deletesecurity")
    with form2:
        ticker = st.selectbox('Remove Ticker', available_tickers)
        # bug_type = cols[1].selectbox(
        #     "Bug type:", ["Front-end", "Back-end", "Data related", "404"], index=2
        # )
        # comment = st.text_area("Comment:")
        # cols = st.columns(2)
        # date = cols[0].date_input("Bug date occurrence:")
        # bug_severity = cols[1].slider("Bug severity:", 1, 5, 2)
        actionDelete = st.form_submit_button(label="REMOVE")

    if actionDelete:
        #db = StockDB('stocks.db')
        #sa = StocksAPI()

        #num = db2.delete_ticker(ticker) 
        db2.delete_ticker(ticker) 

        # db.close()

        st.success(f"{ticker} deleted.")
        st.balloons()
        
        # db = StockDB('stocks.db')
    
        table = db2.db_summary()

        placeholder.table(table)

        # db.close()
        
import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import pandas as pd
import datetime

from StockDB import StockDB 
from StockAPI import StocksAPI
from Accounts import Account

def fetch_and_load_daily(db, api, ticker, outputsize="compact"):
    temp = api.get_daily_series(ticker, outputsize)
    db.insert_daily_data(ticker, temp)

def app():

    st.title('DBAdmin')

    db = StockDB('stocks.db')
    
    table = db.db_summary()

    db.close()

    st.table(table)

    st.write("Add security:")

    form = st.form(key="annotation")

    with form:
        cols = st.columns((1, 1))
        ticker = cols[0].text_input("Ticker:")
        # bug_type = cols[1].selectbox(
        #     "Bug type:", ["Front-end", "Back-end", "Data related", "404"], index=2
        # )
        # comment = st.text_area("Comment:")
        # cols = st.columns(2)
        # date = cols[0].date_input("Bug date occurrence:")
        # bug_severity = cols[1].slider("Bug severity:", 1, 5, 2)
        submitted = st.form_submit_button(label="Submit")


    if submitted:
        db = StockDB('stocks.db')
        sa = StocksAPI()

        fetch_and_load_daily(db, sa, ticker, outputsize='compact')

        db.close()

        st.success("Rows loaded.")
        st.balloons()

    # expander = st.expander("See all records")
    # with expander:
    #     st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    #     st.dataframe(get_data(gsheet_connector))
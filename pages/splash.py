import streamlit as st

def app():
    st.title('Stock Trading momentum App')

    st.header('blurb')

    st.header("Components:")
    
    st.markdown("1. Streamlit (this app)")
    st.markdown("2. Alpha Vantage API (to get stock prices")
    st.markdown("3. Oracle Autonomous Cloud database to collect the stock data and feed the app")
import streamlit as st

from PIL import Image

def app():
    st.title('Stock Trading momentum App')

    col1, col2 = st.columns(1,1)

    image = Image.open('images/pexels-burak-kebapci-187041.jpg')
    col2.image(image, caption = "Photo by Burak Kebapci from Pexels", use_column_width='auto')

    col1.header("Components:")
    
    col1.markdown("1. Streamlit (this app)")
    col1.markdown("2. Alpha Vantage API (to get stock prices")
    col1.markdown("3. Oracle Autonomous Cloud database to collect the stock data and feed the app")
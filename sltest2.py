import streamlit as st

from multipage import MultiPage
from pages import stockhist, dbadmin, splash

app = MultiPage()

st.title('Stock Trend Trading App')

app.add_page("Introduction", splash.app)
app.add_page("Stock History", stockhist.app)
app.add_page('DB Admin', dbadmin.app)

app.run()

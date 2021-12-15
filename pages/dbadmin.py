import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import pandas as pd
import datetime

from StockDB import StockDB 
from Accounts import Account


def app():

    st.title('DBAdmin')

    db = StockDB('stocks.db')
    
    table = db.db_summary()

    db.close()

    st.table(table)
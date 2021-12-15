import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import pandas as pd
import datetime

from StockDB import StockDB 
from Accounts import Account


def app():

    st.title('DBAdmin')

    db = StockDB()
    
    table = db.db_summary()

    db.close()

    st.write(table)
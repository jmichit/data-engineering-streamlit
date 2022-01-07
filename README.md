# Trend Trading the US stock market App

Metis Introduction to Data Engineering project

## Abstract
The goal of this project was to build a tool to allow for quick and easy testing of some simple rules-based trading strategies i.e. strategies based on prior price action (such as [moving averages](https://quantstrategies.academy/2020/08/28/how-to-use-moving-average/#Simple_Moving_Average) ) as opposed to market fundamentals, global economic factors, valuation / earnings ratios etc.  The inspiration for this project is the well known story of the Turtle Traders ( see [Turtle Trading: A Market Legend](https://www.investopedia.com/articles/trading/08/turtle-trading.asp) or [Turtle Trading Strategy](https://vantagepointtrading.com/top-trader-richard-dennis-turtle-trading-strategy/) )

## Design
Oracle REST APIs expose key data functions (loading securities, deleting securites, adding statistics, retrieving database information, etc.) to the Streamlit hosted app which puts control of these functions in the users hands. 
The App allows users to see the impact of simple buy & hold strategy vs. forecasted time series for selected time periods and securities. 

3 Page Streamlit
1) Flash page ([splash.py](https://github.com/jmichit/data-engineering-streamlit/blob/master/pages/splash.py)) - app information
2) Stock History ([stockhist.py](https://github.com/jmichit/data-engineering-streamlit/blob/master/pages/stockhist.py))- Choose ticker and dates and displays graph
3) DB Admin - ([dbadmin.py](https://github.com/jmichit/data-engineering-streamlit/blob/master/pages/dbadmin.py))uploads / deletes stock data via Oracle API endpoints

Main page ([sltest2.py](https://github.com/jmichit/data-engineering-streamlit/blob/master/sltest2.py)) uses Multipage class to allow for page selection from dropdown

Helper classes:
* Multipage ([multipage.py)](https://github.com/jmichit/data-engineering-streamlit/blob/master/multipage.py)) Thanks Praneel Nihar for the description and code in this [article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4) on Medium.
* Calls to Oracle API ([StockDB2.py](https://github.com/jmichit/data-engineering-streamlit/blob/master/StockDB2.py)) to retrieve loaded datasets and load new tickers
* Calls to Alpha Vantage([StockAPI.py](https://github.com/jmichit/data-engineering-streamlit/blob/master/StockAPI.py)) to fetch requested stock data from Alpha Vantage
* Accounts.py manages account information - overkill for one stock but a structure that could be completed to how to handle multiple stock portfolio 

Authorization key for Alpha Vantage stored as Secret in Streamlit setting

## Data
* [Alpha Vantage](https://www.alphavantage.co/) provides free historical stock quotes for US and international equities daily, weekly, monthly,  or even intra-day going back 20 years 

## Technologies
* Streamlit app (hosted on Streamlit Cloud)
* Alpha Vantage Stock API
* Oracle Autonomous Data Warehouse (Cloud) - SQL 
* Oracle REST APIs for interaction between app and database
* Python (matplotlib and seaborn)
* Facebook Prophet python module for time series forecasting

## Communications
1. This abstract
2. Slide deck
3. Code files
4. The publically accessible app 

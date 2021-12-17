# Trend Trading the US stock market App

Metis Introduction to Data Engineering project

## Abstract
The goal of this project was to build a tool to allow for quick and easy testing of some simple rules-based trading strategies i.e. strategies based on prior price action (such as [moving averages](https://quantstrategies.academy/2020/08/28/how-to-use-moving-average/#Simple_Moving_Average) ) as opposed to market fundamentals, global economic factors, valuation / earnings ratios etc.  The inspiration for this project is the well known story of the Turtle Traders ( see [Turtle Trading: A Market Legend](https://www.investopedia.com/articles/trading/08/turtle-trading.asp) or [Turtle Trading Strategy](https://vantagepointtrading.com/top-trader-richard-dennis-turtle-trading-strategy/) )

## Design
Oracle REST APIs expose key data functions (loading securities, deleting securites, adding statistics, retrieving database information, etc.) Streamlit puts control of these functions in the users hands. 
The App allows users to see the impact of simple strategies for selected time periods and securities. 

## Data
* [Alpha Vantage](https://www.alphavantage.co/) provides free historical stock quotes for US and international equities daily, weekly, monthly,  or even intra-day going back 20 years 

## Technologies
* Streamlit app (hosted on Streamlit Cloud)
* Alpha Vantage Stock API
* Oracle Autonomous Data Warehouse (Cloud) - SQL 
* Oracle REST APIs for interaction between app and database
* Python (matplotlib and seaborn)

## Communications
1. This abstract
2. Slide deck
3. Code files
4. The publically accessible app 

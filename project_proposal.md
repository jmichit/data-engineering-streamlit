# US Stock Data trend tracker

<i> John Michitsch </i>

## Background
People make (and often lose) money in the stock market employeeing a wide array of strategies.  One interesting strategy is momentum trading - identifying the trend (lets assume upward - only interested in "going long", buy then sell and hopefully profit from the higher exit price. This is interesting because the strategy ignores fundamental factors (firm profitability, fundamentals, dividend payments, etc.) and relies entirely on price movement.  

## Goal
1) Load prices for basket of stocks (maybe Dow Industrials or S&P 500 or adhoc list)
2) Use price movement to identify best trends
3) (Maybe) try machine learning algorithm to forecast future price
4) Present the data with an interactive and easily understandable web interfade

## Data
US Stock data for select tickers will be obtained from AlphaVantage.com API and loaded into SQLite.
Each trading day data set will be updated with current prices
Original scope will be end of day daily prices and if time allows the MVP may use intra day data, also available through AlphaVantage

## MVP
Flask, Streamlit, or Dash app allowing the user to see stock trend data

# Communications
Presentation deck

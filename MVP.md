# Minimal Viable Product

## Overview

Flask app using a SQLite database pulls daily stock data for various tickers and applies a classic trend trading indicator to enter and exit positions. 

## Database

Current contents of Stock database
<img width="956" alt="image" src="https://user-images.githubusercontent.com/11722304/145901102-9099dcd8-977d-4523-918a-592c866e30a1.png">

## User Interface (work in progress)

<img width="956" alt="image" src="https://user-images.githubusercontent.com/11722304/145901354-85d353e6-c116-44e0-8ae0-22d7a0470b32.png">

Interface allows user to select the ticker, start date, and end date for period to analyze. 

Script generates signals to buy or sell based on 10 day max or 20 day low, respectively. 

## Data updates

Cron job will update the existing tickers after market close and update the signals. 

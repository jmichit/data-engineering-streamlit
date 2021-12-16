import requests

class StocksAPI():
    #Free API key for Alpha Vantage
    
    def __init__(self):
        self.apikey ='6XTDHKAU1QFL7M38'
    
    def get_daily_series(self, ticker, outputsize='compact'):
        """
        Get daily series of prices from Alpha Vantage 

        Head of response.json:  
        {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2021-12-09",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern"},
        "Time Series (Daily)": {
            "2021-12-09": {
                "1. open": "122.1500",
                "2. high": "123.9500",
                "3. low": "121.7900",
                "4. close": "123.5700",
                "5. volume": "4595377"
            },
            "2021-12-08": {
                "1. open": "122.0000",
                "2. high": "123.3800",
                "3. low": "121.5200",
                "4. close": "123.0200",
                "5. volume": "5483948"
            }, ... 
         }
        }
        """

        url = 'https://www.alphavantage.co/query'

        params = {'function':'TIME_SERIES_DAILY',
                  'symbol': ticker,
                  'outputsize' : outputsize,    
                  'apikey': self.apikey}

        response = requests.get(url, params=params)

        data  = response.json()

        fname = 'compact-' + ticker + '.pkl'
        with open(fname, 'wb') as file:
            pkl.dump(data, file )

        dailyprices = data['Time Series (Daily)']

        #We are using the daily close price    
        prices = [(x, float(dailyprices[x]['4. close'])) for x in dailyprices.keys()]

        return prices

import requests
import pandas as pd
import mplfinance as mpf
import api

function = "TIME_SERIES_DAILY"
symbol = "PETR4.SA"
url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api.key}"
json = requests.get(url).json()

data = {
    'date': [],
    'open': [],
    'high': [],
    'low': [],
    'close': [],
    'volume': []
}

# not optimal but the best way I found to create the pandas dataframe
for day in json["Time Series (Daily)"]:
    data['date'].append(day)
    data['open'].append(
        float(json["Time Series (Daily)"][f"{day}"]["1. open"]))
    data['high'].append(
        float(json["Time Series (Daily)"][f"{day}"]["2. high"]))
    data['low'].append(float(json["Time Series (Daily)"][f"{day}"]["3. low"]))
    data['close'].append(
        float(json["Time Series (Daily)"][f"{day}"]["4. close"]))
    data['volume'].append(
        float(json["Time Series (Daily)"][f"{day}"]["5. volume"]))

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
# inverts the column order to make the oldest values come first
df = df.iloc[::-1]

mpf.plot(df, type="candle", mav=(20), volume=True,
         style="yahoo", title=f"{symbol}")

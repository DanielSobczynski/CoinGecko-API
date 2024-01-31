#This is a project designated for creating Candlestick Chart of bitcoin price from last three months. It was done using CoinGecko API.

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc

#Getting the data from CoinGecko using API
cg = CoinGeckoAPI()
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=90)

#Selecting data
bitcoin_price_data = bitcoin_data['prices']

#Turning this data into a Pandas DataFrame.
data = pd.DataFrame(bitcoin_price_data, columns=['TimeStamp', 'Price'])

#Converting the timestamp to readable datetime.
data['date'] = data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))

#Grouping by the Date and finding the min, max, open, and close for the candlesticks.
candlestick_data = data.groupby(data.date, as_index=False).agg({"Price": ['min', 'max', 'first', 'last']})

#Creating Candlestick Chart
fig = go.Figure(data=[go.Candlestick(x=candlestick_data['date'],
                open=candlestick_data['Price']['first'],
                high=candlestick_data['Price']['max'],
                low=candlestick_data['Price']['min'],
                close=candlestick_data['Price']['last'])
                ])

fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()
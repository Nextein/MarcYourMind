# =====================================================
#               Author: Marc Goulding
#               gouldingmarc@gmail.com
# =====================================================

"""
Usage:
    Check you are at the top level directory.
    run:
        > python -m plutus.top_movers_scanner

"""

from time import time
import numpy as np
from pprint import pprint
import pandas as pd

import binance


client = binance.client.Client()

tickers = client.get_ticker()

print("Starting scan...")
btc_tickers = []
busd_tickers = []
for ticker in tickers:
    if 'BTC' in ticker['symbol'] and not ticker['symbol'].startswith('BTC'):
        btc_tickers.append(ticker)
    if 'BUSD' in ticker['symbol'] and not ticker['symbol'].startswith('BUSD'):
        busd_tickers.append(ticker)

btc_tickers = sorted(btc_tickers, key=lambda k: float(k['priceChangePercent']))
busd_tickers = sorted(busd_tickers, key=lambda k: float(k['priceChangePercent']))

btc_symbols = [ticker['symbol'] for ticker in btc_tickers]
busd_symbols = [ticker['symbol'] for ticker in busd_tickers]

print("\n(**BTC**) Top 20 longs:")
for i in np.arange(-1, -21, -1):
    print(btc_symbols[i], '\t\t', btc_tickers[i]['priceChangePercent'])
print("\n(**BTC**) Top 20 shorts:")
for i in range(20):
    print(btc_symbols[i], '\t\t', btc_tickers[i]['priceChangePercent'])

print("\n(**BUSD**) Top 20 longs:")
for i in np.arange(-1, -21, -1):
    print(busd_symbols[i], '\t\t', busd_tickers[i]['priceChangePercent'])
print("\n(**BUSD**) Top 20 shorts:")
for i in range(20):
    print(busd_symbols[i], '\t\t', busd_tickers[i]['priceChangePercent'])

# read csv
btc_directory = "plutus/resources/logs/top_moversBTC.csv"
busd_directory = "plutus/resources/logs/top_moversBUSD.csv"
try:
    btc_movers = pd.read_csv(btc_directory)
    btc_index = btc_movers.iloc[-1]['index'] + 1
except FileNotFoundError:
    # Create pandas
    btc_movers = pd.DataFrame([], columns=['index', 'time', '1long', '2long', '3long', '4long', '5long', '6long', '7long', '8long', '9long', '10long', '11long', '12long', '13long', '14long', '15long', '16long', '17long', '18long', '19long', '20long', '1short', '2short', '3short', '4short', '5short', '6short', '7short', '8short', '9short', '10short', '11short', '12short', '13short', '14short', '15short', '16short', '17short', '18short', '19short', '20short'])
    btc_index = 0
try:
    busd_movers = pd.read_csv(busd_directory)
    busd_index = busd_movers.iloc[-1]['index'] + 1
except FileNotFoundError:
    busd_movers = pd.DataFrame([], columns=['index', 'time', '1long', '2long', '3long', '4long', '5long', '6long', '7long', '8long', '9long', '10long', '11long', '12long', '13long', '14long', '15long', '16long', '17long', '18long', '19long', '20long', '1short', '2short', '3short', '4short', '5short', '6short', '7short', '8short', '9short', '10short', '11short', '12short', '13short', '14short', '15short', '16short', '17short', '18short', '19short', '20short'])
    busd_index = 0

# append row to csv
toplongs = btc_symbols[-20:]
toplongs.reverse()
topshorts = btc_symbols[:20]
new_entry = [btc_index, time()] + toplongs + topshorts
btc_movers.loc[len(btc_movers)] = new_entry
# save csv
btc_movers.to_csv(btc_directory, index=False)
print(f"Saved to {btc_directory}")

toplongs = busd_symbols[-20:]
toplongs.reverse()
topshorts = busd_symbols[:20]
new_entry = [busd_index, time()] + toplongs + topshorts
busd_movers.loc[len(busd_movers)] = new_entry
# save csv
busd_movers.to_csv(busd_directory, index=False)
print(f"Saved to {busd_directory}")

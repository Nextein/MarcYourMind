import utils
from time import time
import numpy as np
import binance


# Function to retrieve top movers
def get_top_movers(tickers):
    movers = sorted(tickers, key=lambda k: float(k['priceChangePercent']))
    symbols = [ticker['symbol'] for ticker in movers]
    top_longs = symbols[-20:][::-1]  # Top 20 longs, reversed for ascending order
    top_shorts = symbols[:20]  # Top 20 shorts
    return top_longs, top_shorts

# Function to store data in Firestore
def store_top_movers(collection_name, top_longs, top_shorts):
    # Create a new document with current timestamp as the document ID
    doc_ref = utils.db.collection(collection_name).document(str(int(time())))
    doc_ref.set({
        'top_longs': top_longs,
        'top_shorts': top_shorts
    })

# Fetch tickers from Binance
client = binance.client.Client()
tickers = client.get_ticker()

# Retrieve top movers for BTC and BUSD
btc_tickers = [ticker for ticker in tickers if 'BTC' in ticker['symbol'] and not ticker['symbol'].startswith('BTC')]
busd_tickers = [ticker for ticker in tickers if 'BUSD' in ticker['symbol'] and not ticker['symbol'].startswith('BUSD')]

btc_longs, btc_shorts = get_top_movers(btc_tickers)
busd_longs, busd_shorts = get_top_movers(busd_tickers)

# Store data in Firestore
store_top_movers('btc_movers', btc_longs, btc_shorts)
store_top_movers('busd_movers', busd_longs, busd_shorts)

print("Data stored successfully in Firestore.")

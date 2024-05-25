import utils
from datetime import datetime
import numpy as np
import binance

# Function to retrieve top movers
def get_top_movers(tickers):
    movers = sorted(tickers, key=lambda k: float(k['priceChangePercent']))
    symbols = [ticker['symbol'] for ticker in movers]
    percent_changes = [float(ticker['priceChangePercent']) for ticker in movers]  # Extract percentChange
    top_longs = symbols[-20:][::-1]  # Top 20 longs, reversed for ascending order
    top_shorts = symbols[:20]  # Top 20 shorts
    percent_changes_longs = percent_changes[-20:][::-1]  # Corresponding percentChange for longs
    percent_changes_shorts = percent_changes[:20]  # Corresponding percentChange for shorts
    return (top_longs, top_shorts), (percent_changes_longs, percent_changes_shorts)

# Function to store data in Firestore
def store_top_movers(collection_name, top_movers, percent_changes, date):
    # Create a new document with today's date as the document ID
    doc_ref = utils.db.collection(collection_name).document(date)
    doc_ref.set({
        'top_longs': top_movers[0],
        'top_shorts': top_movers[1],
        'percent_changes_longs': percent_changes[0],
        'percent_changes_shorts': percent_changes[1]
    })

# Fetch tickers from Binance
client = binance.client.Client()
tickers = client.get_ticker()

# Get today's date
today_date = datetime.now().strftime("%Y-%m-%d")

# Retrieve top movers for BTC and USD
btc_tickers = [ticker for ticker in tickers if ticker['symbol'].endswith('BTC') and not ticker['symbol'].startswith('BTC')]
usd_tickers = [ticker for ticker in tickers if ticker['symbol'].endswith('USDC') and not ticker['symbol'].startswith('USD')]

(btc_longs, btc_shorts), (btc_percent_changes_longs, btc_percent_changes_shorts) = get_top_movers(btc_tickers)
(usd_longs, usd_shorts), (usd_percent_changes_longs, usd_percent_changes_shorts) = get_top_movers(usd_tickers)

# Store data in Firestore with today's date as the document ID
store_top_movers('btc_movers', (btc_longs, btc_shorts), (btc_percent_changes_longs, btc_percent_changes_shorts), today_date)
store_top_movers('usd_movers', (usd_longs, usd_shorts), (usd_percent_changes_longs, usd_percent_changes_shorts), today_date)

print("Data stored successfully in Firestore for today:", today_date)

import pandas as pd
from binance.client import Client

def new_client(name=None):
    """Creates a new Binance client for api access to the account"""
    # print("WARNING - Binance.new_client(name) loads basic account regardless of name given.")
    client = Client()
    # api_key=config[name]['api_key'],
                    # api_secret=config[name]['secret_key'])
    return client



def get_current_data(ticker, interval, lookback=None, start=None, verbose=False, client=None) -> pd.DataFrame:
    """
    Can only handle lookback in days.

    args:
        ticker: string
        lookback: can be number of days to fetch or a string as specified by binance api.
        start: alternative input to lookback. Used when lookback is a Unix timestamp
    """

    if client is None:
        client = new_client('test@account')

    if lookback:
        if type(lookback) == int:
            ohlcv = client.get_historical_klines(ticker, interval, f"{lookback} days ago UTC")
        elif type(lookback) == str:
            ohlcv = client.get_historical_klines(ticker, interval, lookback)
    elif start:
        if type(start) == int:
            ohlcv = client.get_historical_klines(ticker, interval, start)
    else:
        raise Exception("Invalid 'lookback' or 'start' parameter given.")
    data = pd.DataFrame(ohlcv, columns=['open time',
                                        'Open',
                                        'High',
                                        'Low',
                                        'Close',
                                        'Volume',
                                        'close time',
                                        'asset volume',
                                        '# trades',
                                        'base buy volume',
                                        'quote buy volume',
                                        'ignore'])

    data = data.drop(columns=['close time', 'asset volume', 'base buy volume', 'quote buy volume', 'ignore', '# trades'])

    data['Open'] = data['Open'].astype(float)
    data['High'] = data['High'].astype(float)
    data['Low'] = data['Low'].astype(float)
    data['Close'] = data['Close'].astype(float)
    data['Volume'] = data['Volume'].astype(float)
    data['open time'] = pd.to_datetime(data['open time'], unit='ms')
    if verbose:
        print(data.head(15))
    return data

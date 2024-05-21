import utils
import pandas as pd # type: ignore
import numpy as np # type: ignore
import binance

def in_order(data1, data2, is_value=0) -> bool:
    """ Check if last candle in data1 is above last candle in data2"""
    if not is_value:
        return data1.iloc[-1] > data2.iloc[-1]
    elif is_value == 1:
        return data1 > data2.iloc[-1]
    elif is_value == 2:
        return data1.iloc[-1] > data2
    elif is_value == 3:
        return data1 > data2

def greenCandle(data, i=-1) -> bool:
    """ Green Candle """
    return data.iloc[i]['Close'] > data.iloc[i]['Open']

def redCandle(data, i=-1) -> bool:
    """ Red Candle """
    return data.iloc[i]['Close'] < data.iloc[i]['Open']

def HH(data, i) -> bool:
    """ Last 2 candles make a Higher High """
    return in_order(data.iloc[i]['High'], data.iloc[i-1]['High'], is_value=3)

def HL(data, i) -> bool:
    """ Last 2 candles make a Higher Low """
    return in_order(data.iloc[i]['Low'], data.iloc[i-1]['Low'], is_value=3)

def LL(data, i) -> bool:
    """ Last 2 candles make a Lower Low """
    return in_order(data.iloc[i-1]['Low'], data.iloc[i]['Low'], is_value=3)

def LH(data, i) -> bool:
    """ Last 2 candles make a Lower High """
    return in_order(data.iloc[i-1]['High'], data.iloc[i]['High'], is_value=3)

def relativePositionOfCandles(data):
    """
    Tag candles with a state between:

    up, down, reverse-up, reverse-down, reverse-up2, reverse-down2, indecision, indecision2
    or undefined. ( U-D-RU-RD-RU2-RD2-I-I2-X )

    States are defined based on position relative to previous candlestick (Higher Highs or Lower Lows etc).
    """
    state = ['X' for i in range(data.shape[0])]

    # Identify state for each candle based on previous candle's state
    for i in range(2, data.shape[0]):
        if state[i-1] == 'X':
            if HH(data, i) and HL(data, i):
                state[i] = 'U'
            elif LH(data, i) and LL(data, i):
                state[i] = 'D'
            elif LH(data, i) and HL(data, i):
                if LH(data, i-1) and HL(data, i-1):
                    state[i] = 'I2'
                else:
                    state[i] = 'I'
            elif HH(data, i) and LL(data, i):
                if greenCandle(data, i):
                    state[i] = 'RU2'
                elif redCandle(data, i):
                    state[i] = 'RD2'
        elif state[i-1] == 'U':
            if HH(data, i) and HL(data, i):
                state[i] = 'U'
            elif LH(data, i) and LL(data, i):
                state[i] = 'RD'
            elif LH(data, i) and HL(data, i):
                if LH(data, i-1) and HL(data, i-1):
                    state[i] = 'I2'
                else:
                    state[i] = 'I'
            elif HH(data, i) and LL(data, i):
                state[i] = 'RU'
        elif state[i-1] == 'D':
            if HH(data, i) and HL(data, i):
                state[i] = 'RU'
            elif LH(data, i) and LL(data, i):
                state[i] = 'D'
            elif LH(data, i) and HL(data, i):
                if LH(data, i-1) and HL(data, i-1):
                    state[i] = 'I2'
                else:
                    state[i] = 'I'
            elif HH(data, i) and LL(data, i):
                state[i] = 'RU'
        elif state[i-1] == 'RU' or state[i-1] == 'RU2':
            if HH(data, i) and HL(data, i):
                state[i] = 'U'
            elif LH(data, i) and LL(data, i):
                state[i] = 'RD'
            elif LH(data, i) and HL(data, i):
                if LH(data, i-1) and HL(data, i-1):
                    state[i] = 'I2'
                else:
                    state[i] = 'I'
            elif HH(data, i) and LL(data, i):
                if greenCandle(data, i):
                    state[i] = 'RU2'
                elif redCandle(data, i):
                    state[i] = 'RD2'
        elif state[i-1] == 'RD' or state[i-1] == 'RD2':
            if HH(data, i) and HL(data, i):
                state[i] = 'RU'
            elif LH(data, i) and LL(data, i):
                state[i] = 'D'
            elif LH(data, i) and HL(data, i):
                if LH(data, i-1) and HL(data, i-1):
                    state[i] = 'I'
                else:
                    state[i] = 'I'
            elif HH(data, i) and LL(data, i):
                if greenCandle(data, i):
                    state[i] = 'RU2'
                elif redCandle(data, i):
                    state[i] = 'RD2'
        elif state[i-1] == 'I':
            if HH(data, i) and HL(data, i):
                state[i] = 'RU'
            elif LH(data, i) and LL(data, i):
                state[i] = 'RD'
            elif LH(data, i) and HL(data, i):
                state[i] = 'I2'
            elif HH(data, i) and LL(data, i):
                if greenCandle(data, i):
                    state[i] = 'RU2'
                elif redCandle(data, i):
                    state[i] = 'RD2'
        elif state[i-1] == 'I2':
            if HH(data, i) and HL(data, i):
                state[i] = 'RU'
            elif LH(data, i) and LL(data, i):
                state[i] = 'RD'
            elif LH(data, i) and HL(data, i):
                state[i] = 'I2'
            elif HH(data, i) and LL(data, i):
                if greenCandle(data, i):
                    state[i] = 'RU2'
                elif redCandle(data, i):
                    state[i] = 'RD2'
        else:
            print(f"Strategy FSM in unkown state: {state[i]}")
            exit()
    return state

def relativeCandlesPhases(data):
    """
    Direction Phases based on relative candles.
    args:
        data
    """
    tags = relativePositionOfCandles(data)
    phase = np.zeros(data.shape[0])
    
    phase[0] = 1 if greenCandle(data,0) else -1
    for i in range(1, 3):
        phase[i] = phase[i-1]

    for i in range(3,data.shape[0]):
        state2, state1, state0 = tags[i-2], tags[i-1], tags[i]
        up_sequences = [
            state1 == 'D'  and state0 == 'RU',
            state1 == 'D'  and state0 == 'RU2',
            state1 == 'RD' and state0 == 'RU',
            state1 == 'RD' and state0 == 'RU2',
            state1 == 'RD2' and state0 == 'RU',
            state1 == 'RD2' and state0 == 'RU2',
            state2 == 'D'  and state1 == 'I' and state0 == 'RU',
            state2 == 'D'  and state1 == 'I' and state0 == 'RU2',
            state2 == 'RD' and state1 == 'I' and state0 == 'RU',
            state2 == 'RD' and state1 == 'I' and state0 == 'RU2',
            state2 == 'RD2' and state1 == 'I' and state0 == 'RU',
            state2 == 'RD2' and state1 == 'I' and state0 == 'RU2',
            state2 == 'I' and state1 == 'I2' and state0 == 'RU',
            state2 == 'I' and state1 == 'I2' and state0 == 'RU2',
        ]

        down_sequences = [
            state1 == 'U'  and state0 == 'RD',
            state1 == 'U'  and state0 == 'RD2',
            state1 == 'RU' and state0 == 'RD',
            state1 == 'RU' and state0 == 'RD2',
            state1 == 'RU2' and state0 == 'RD2',
            state1 == 'RU2' and state0 == 'RD',
            state2 == 'U'  and state1 == 'I' and state0 == 'RD',
            state2 == 'U'  and state1 == 'I' and state0 == 'RD2',
            state2 == 'RU' and state1 == 'I' and state0 == 'RD',
            state2 == 'RU' and state1 == 'I' and state0 == 'RD2',
            state2 == 'RU2' and state1 == 'I' and state0 == 'RD',
            state2 == 'RU2' and state1 == 'I' and state0 == 'RD2',
            state2 == 'I' and state1 == 'I2' and state0 == 'RD',
            state2 == 'I' and state1 == 'I2' and state0 == 'RD2',
        ]

        # Check phase up sequence:
        if any(up_sequences):
            phase[i] = 1
            if state1 == 'I':
                phase[i-1] = 1
            if state1 == 'I2':
                phase[i-1] = 1
                phase[i-2] = 1
            if state1 == 'RD':
                phase[i-1] = 1
            if state1 == 'RD2':
                phase[i-1] = 1
                phase[i-2] = 1
        # Check phase down sequence:
        elif any(down_sequences):
            phase[i] = -1
            if state1 == 'I':
                phase[i-1] = -1
            if state1 == 'I2':
                phase[i-1] = -1
                phase[i-2] = -1
            if state1 == 'RU':
                phase[i-1] = -1
            if state1 == 'RU2':
                phase[i-1] = -1
                phase[i-2] = -1
        else:
            phase[i] = phase[i-1]
    return phase


def split_into_sets(data, states, value):
    sets = []
    current_set_indices = []
    for i, state in enumerate(states):
        if state == value:
            current_set_indices.append(i)
        else:
            if current_set_indices:
                sets.append(current_set_indices)
                current_set_indices = []
    # Append the last set if it exists
    if current_set_indices:
        sets.append(current_set_indices)
    return sets



client = binance.client.Client()

tickers = client.get_ticker()

print("Starting scan...")
btc_tickers = []
busd_tickers = []
for ticker in tickers:
    if ticker['symbol'].endswith('BTC'):
        btc_tickers.append(ticker)
    if ticker['symbol'].endswith('BUSD'):
        busd_tickers.append(ticker)

btc_tickers = sorted(btc_tickers, key=lambda k: float(k['priceChangePercent']))
busd_tickers = sorted(busd_tickers, key=lambda k: float(k['priceChangePercent']))

btc_symbols = [ticker['symbol'] for ticker in btc_tickers]
busd_symbols = [ticker['symbol'] for ticker in busd_tickers]

# Params
# ticker = 'BTCUSDT'

# Backup collections and clear them
utils.backup_collection("cycles_down", "cycles_down_history")
utils.backup_collection("cycles_up", "cycles_up_history")

utils.deleteCollection("cycles_down")
utils.deleteCollection("cycles_up")

interval = '1h'
lookback = 60
for ticker in btc_symbols+busd_symbols:

    
    try:
        print('-'*20)
        print(ticker)
        # Read data
        data = utils.get_current_data(ticker, interval, lookback)

        # Apply the indicator
        states = relativeCandlesPhases(data)

        print("States:")
        print(states)

        # Split data into sets of state 1 and state -1
        sets_state_1 = split_into_sets(data, states, 1)
        sets_state_minus_1 = split_into_sets(data, states, -1)

        print("sets:")
        print("State 1:")
        print(sets_state_1[-2:])
        print('-'*20)
        print("State -1:")
        print(sets_state_minus_1[-2:])

        phases_1 = sets_state_1[-2:]
        phases_minus_1 = sets_state_minus_1[-2:]

        print("Corresponding data:")
        print("State 1:")
        print(data.iloc[phases_1[0][0]:phases_1[0][-1]+1])
        print(data.iloc[phases_1[1][0]:phases_1[1][-1]+1])
        print('-'*20)
        print("State -1:")
        print(data.iloc[phases_minus_1[0][0]:phases_minus_1[0][-1]+1])
        print(data.iloc[phases_minus_1[1][0]:phases_minus_1[1][-1]+1])

        if (data.iloc[phases_1[0][0]]['open time'] < data.iloc[phases_minus_1[0][0]]['open time']):
            print("State 1 starts first.")
            A = data.iloc[phases_1[0][0]:phases_1[0][-1]+1]
            B = data.iloc[phases_minus_1[0][0]:phases_minus_1[0][-1]+1]
            C = data.iloc[phases_1[1][0]:phases_1[1][-1]+1]
            D = data.iloc[phases_minus_1[1][0]:phases_minus_1[1][-1]+1]
        else:
            print("State -1 starts first.")
            A = data.iloc[phases_minus_1[0][0]:phases_minus_1[0][-1]+1]
            B = data.iloc[phases_1[0][0]:phases_1[0][-1]+1]
            C = data.iloc[phases_minus_1[1][0]:phases_minus_1[1][-1]+1]
            D = data.iloc[phases_1[1][0]:phases_1[1][-1]+1]

        # Check if CD has a higher high and a higher low than AB
        higher_high = max(C['High'].max(), D['High'].max()) > max(A['High'].max(), B['High'].max())
        higher_low = min(C['Low'].min(), D['Low'].min()) > min(A['Low'].min(), B['Low'].min())

        # Check if CD has a lower high and a lower low
        lower_high = max(C['High'].max(), D['High'].max()) < max(A['High'].max(), B['High'].max())
        lower_low = min(C['Low'].min(), D['Low'].min()) < min(A['Low'].min(), B['Low'].min())

        # Check if both conditions are met
        if higher_high and higher_low:
            print("CD has a higher high and a higher low than AB.")
            data = {
                "ticker": ticker,
                "price": data.iloc[-1]['Close'],
                "date": utils.get_current_date()
            }
            utils.createDocument('cycles_up', data=data)
        if lower_high and lower_low:
            print("CD has a lower high and a lower low than AB.")
            data = {
                "ticker": ticker,
                "price": data.iloc[-1]['Close'],
                "date": utils.get_current_date()
            }
            utils.createDocument('cycles_down', data=data)
    except Exception as e:
        print(f"Failed for {ticker}.")
        continue

print("Scan completed.")
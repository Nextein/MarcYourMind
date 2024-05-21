import utils
import pandas as pd

def greenCandle(self, data, i=-1) -> bool:
        """ Green Candle """
        return data.iloc[i]['Close'] > data.iloc[i]['Open']

def redCandle(self, data, i=-1) -> bool:
    """ Red Candle """
    return data.iloc[i]['Close'] < data.iloc[i]['Open']

def HH(self, data, i) -> bool:
    """ Last 2 candles make a Higher High """
    return self.in_order(data.iloc[i]['High'], data.iloc[i-1]['High'], is_value=3)

def HL(self, data, i) -> bool:
    """ Last 2 candles make a Higher Low """
    return self.in_order(data.iloc[i]['Low'], data.iloc[i-1]['Low'], is_value=3)

def LL(self, data, i) -> bool:
    """ Last 2 candles make a Lower Low """
    return self.in_order(data.iloc[i-1]['Low'], data.iloc[i]['Low'], is_value=3)

def LH(self, data, i) -> bool:
    """ Last 2 candles make a Lower High """
    return self.in_order(data.iloc[i-1]['High'], data.iloc[i]['High'], is_value=3)

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

# Params
ticker = 'BTCUSDT'
interval = '1h'
lookback = 150

# Read data
data = utils.get_current_data(ticker, interval, lookback)

# Apply the indicator
states = relativePositionOfCandles(data)

# Find groups of up moves and down moves
up_moves = []
down_moves = []
current_move = []
for i, state in enumerate(states):
    if state in ['U', 'RU', 'RU2', 'I', 'I2']:
        current_move.append((i, state))
    elif current_move:
        if any(s in ['D', 'RD'] for _, s in current_move):
            down_moves.append(current_move)
        else:
            up_moves.append(current_move)
        current_move = []

# Select the last 2 sets of up moves and down moves
last_two_up_moves = up_moves[-2:]
last_two_down_moves = down_moves[-2:]

# Print the last 2 sets of up moves and down moves
print("Last two sets of up moves:")
for move in last_two_up_moves:
    print(move)
print("\nLast two sets of down moves:")
for move in last_two_down_moves:
    print(move)
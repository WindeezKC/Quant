import numpy as np
import pandas as pd

class Strategy:
    def __init__(self, name):
        self.name = name

    def generate_signals(self, data):
        raise NotImplementedError("Should implement generate_signals method")

class AdvancedStrategy(Strategy):
    def __init__(self, rsi_period=14, bollinger_bands_period=20, rsi_overbought=70, rsi_oversold=30):
        super().__init__("Advanced Strategy")
        self.rsi_period = rsi_period
        self.bollinger_bands_period = bollinger_bands_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        # Calculate RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        signals['rsi'] = 100 - (100 / (1 + rs))

        # Calculate Bollinger Bands
        signals['middle_band'] = data['close'].rolling(window=self.bollinger_bands_period).mean()
        signals['std_dev'] = data['close'].rolling(window=self.bollinger_bands_period).std()
        signals['upper_band'] = signals['middle_band'] + (signals['std_dev'] * 2)
        signals['lower_band'] = signals['middle_band'] - (signals['std_dev'] * 2)

        # Generate signals
        signals['signal'][self.rsi_period:] = np.where(
            (signals['rsi'][self.rsi_period:] < self.rsi_oversold) &
            (data['close'][self.rsi_period:] < signals['lower_band'][self.rsi_period:]),
            1.0, 0.0)

        signals['signal'][self.rsi_period:] = np.where(
            (signals['rsi'][self.rsi_period:] > self.rsi_overbought) &
            (data['close'][self.rsi_period:] > signals['upper_band'][self.rsi_period:]),
            -1.0, signals['signal'][self.rsi_period:])

        signals['positions'] = signals['signal'].diff()
        
        return signals

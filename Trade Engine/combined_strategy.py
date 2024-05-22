import numpy as np
import pandas as pd
from strategy import Strategy

class CombinedStrategy(Strategy):
    def __init__(self, rsi_period=14, bollinger_bands_period=20, short_window=40, long_window=100, rsi_overbought=70, rsi_oversold=30, stop_loss=0.05, max_drawdown=0.20):
        super().__init__("Combined Strategy")
        self.rsi_period = rsi_period
        self.bollinger_bands_period = bollinger_bands_period
        self.short_window = short_window
        self.long_window = long_window
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.stop_loss = stop_loss
        self.max_drawdown = max_drawdown

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        # Calculate RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        signals['rsi'] = 100 - (100 / (1 + rs))

        # Calculate Moving Averages
        signals['short_mavg'] = data['close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = data['close'].rolling(window=self.long_window, min_periods=1, center=False).mean()

        # Generate signals
        signals['signal'] = np.where(
            ((signals['rsi'] < self.rsi_oversold) & (signals['short_mavg'] > signals['long_mavg'])),
            1.0, 
            np.where(
                ((signals['rsi'] > self.rsi_overbought) & (signals['short_mavg'] < signals['long_mavg'])),
                -1.0,
                0.0
            )
        )
        
        signals['positions'] = signals['signal'].diff()
        
        return signals

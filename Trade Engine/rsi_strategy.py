import pandas as pd
from strategy import Strategy

class RSIStrategy(Strategy):
    def __init__(self, window=14, overbought=70, oversold=30):
        super().__init__("RSI Strategy")
        self.window = window
        self.overbought = overbought
        self.oversold = oversold

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        signals['rsi'] = rsi
        signals['signal'][rsi < self.oversold] = 1.0  # Buy signal
        signals['signal'][rsi > self.overbought] = -1.0  # Sell signal
        signals['positions'] = signals['signal'].diff()
        return signals

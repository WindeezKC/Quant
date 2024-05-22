import pandas as pd

class Backtest:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data

    def run(self):
        signals = self.strategy.generate_signals(self.data)
        initial_capital = 100000.0
        positions = pd.DataFrame(index=signals.index).fillna(0.0)
        portfolio = pd.DataFrame(index=signals.index).fillna(0.0)

        positions['AAPL'] = 10 * signals['signal']
        portfolio['positions'] = (positions.multiply(self.data['close'], axis=0)).sum(axis=1)
        portfolio['cash'] = initial_capital - (positions.diff().multiply(self.data['close'], axis=0)).sum(axis=1).cumsum()
        portfolio['total'] = portfolio['positions'] + portfolio['cash']
        portfolio['returns'] = portfolio['total'].pct_change()

        return portfolio

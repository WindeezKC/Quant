import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
from data import get_historical_data
from account import Account
from engine import TradeEngine
from combined_strategy import CombinedStrategy

def main():
    account = Account(account_id="ACC123", balance=100000.0)
    strategy = CombinedStrategy(rsi_period=14, bollinger_bands_period=20, short_window=40, long_window=100, rsi_overbought=70, rsi_oversold=30)
    # Can change symbol to anything, Chose apple as its a very good business and stock to look at 
    #with enoguh trading volume 
    symbol = 'AAPL'
    
    # Get historical data 
    historical_data = get_historical_data(symbol, '2024-05-01', '2024-05-03')
    engine = TradeEngine(account, strategy)
    
    # Apply strategy on historical data to train and simulate trading
    engine.run(historical_data)
    
    # Setup initial plot
    fig = go.FigureWidget()
    fig.add_scatter(x=historical_data.index, y=historical_data['close'], mode='lines', name='Close Price')
    fig.update_layout(title='Trading Visualization from 2021 to 2024', showlegend=True)
    fig.show()

    # Plot buy signals
    buy_signals = pd.DataFrame(engine.buy_signals, columns=['time', 'price'])
    sell_signals = pd.DataFrame(engine.sell_signals, columns=['time', 'price'])

    if not buy_signals.empty:
        fig.add_scatter(x=buy_signals['time'], y=buy_signals['price'], mode='markers', name='Buy Signal', marker=dict(color='green', size=10, symbol='triangle-up'))

    if not sell_signals.empty:
        fig.add_scatter(x=sell_signals['time'], y=sell_signals['price'], mode='markers', name='Sell Signal', marker=dict(color='red', size=10, symbol='triangle-down'))

    # Print final account value
    if not sell_signals.empty:
        final_price = sell_signals.iloc[-1]['price']
    else:
        final_price = historical_data.iloc[-1]['close']

    current_prices = {symbol: final_price}
    total_value = account.get_total_value(current_prices)
    print(f"Final account value: ${total_value:.2f}")

if __name__ == "__main__":
    main()

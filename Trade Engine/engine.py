from order import Order
from account import Account

class TradeEngine:
    def __init__(self, account, strategy):
        self.account = account
        self.strategy = strategy
        self.buy_signals = []
        self.sell_signals = []
        self.most_recent_buy_price = None
        self.shares_held = 0  # Track the number of shares currently held
        self.initial_balance = account.balance

    def execute_order(self, order):
        if order.order_type == 'buy':
            self.account.update_balance(-order.price * order.quantity)
            self.account.update_position(order.symbol, order.quantity)
            self.shares_held += order.quantity  # Increase the shares held
            self.buy_signals.append((order.order_id, order.price))
            self.most_recent_buy_price = order.price  # Track the most recent buy price
        elif order.order_type == 'sell':
            if self.shares_held >= order.quantity:
                self.account.update_balance(order.price * order.quantity)
                self.account.update_position(order.symbol, -order.quantity)
                self.shares_held -= order.quantity  # Decrease the shares held
                self.sell_signals.append((order.order_id, order.price))
                # Calculate profit or loss
                if self.most_recent_buy_price is not None:
                    profit_loss = (order.price - self.most_recent_buy_price) * order.quantity
                    profitable = "profitable" if profit_loss > 0 else "not profitable"
                    print(f"The most recent sell was {profitable} with a profit/loss of ${profit_loss:.2f}")
                # Print account value after each sell
                current_prices = {order.symbol: order.price}
                total_value = self.account.get_total_value(current_prices)
                print(f"Total account value after sell: ${total_value:.2f}")
            else:
                print(f"Attempted to sell {order.quantity} shares, but only {self.shares_held} shares are held. Sell order skipped.")
        print(f"Executed {order}")
        print(f"Shares held: {self.shares_held}")  # Print the current number of shares held

    def run(self, data):
        signals = self.strategy.generate_signals(data)
        for date, signal in signals.iterrows():
            current_price = data.loc[date, 'close']
            if signal['positions'] == 1.0:
                order = Order(order_id=date, symbol='AAPL', quantity=50, order_type='buy', price=current_price)
                self.execute_order(order)
            elif signal['positions'] == -1.0:
                order = Order(order_id=date, symbol='AAPL', quantity=50, order_type='sell', price=current_price)
                self.execute_order(order)
            elif self.most_recent_buy_price is not None and current_price <= self.most_recent_buy_price * (1 - self.strategy.stop_loss):
                # Trigger stop-loss
                if self.shares_held > 0:
                    order = Order(order_id=date, symbol='AAPL', quantity=50, order_type='sell', price=current_price)
                    self.execute_order(order)
            # Check for maximum drawdown
            current_balance = self.account.balance
            if current_balance < self.initial_balance * (1 - self.strategy.max_drawdown):
                print(f"Maximum drawdown reached. Current balance: ${current_balance:.2f}")
                break

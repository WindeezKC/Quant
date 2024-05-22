class Account:
    def __init__(self, account_id, balance=0.0):
        self.account_id = account_id
        self.balance = balance
        self.positions = {}  # symbol -> quantity

    def update_balance(self, amount):
        self.balance += amount

    def update_position(self, symbol, quantity):
        if symbol in self.positions:
            self.positions[symbol] += quantity
        else:
            self.positions[symbol] = quantity

    def get_total_value(self, current_prices):
        total_value = self.balance
        for symbol, quantity in self.positions.items():
            if symbol in current_prices:
                total_value += quantity * current_prices[symbol]
        return total_value

    def __repr__(self):
        return f"Account({self.account_id}, {self.balance}, {self.positions})"

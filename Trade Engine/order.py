class Order:
    def __init__(self, order_id, symbol, quantity, order_type, price=None):
        self.order_id = order_id
        self.symbol = symbol
        self.quantity = quantity
        self.order_type = order_type  # 'buy' or 'sell', maybe add mrore late on
        self.price = price

    def __repr__(self):
        return f"Order({self.order_id}, {self.symbol}, {self.quantity}, {self.order_type}, {self.price})"

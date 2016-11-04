from decimal import Decimal

class Algorithm(object):
    def __init__(self, order_book):
        self.active = False
        self.order_book = order_book

    def process_order(self, line, trade, order):
        tokens = line.strip().split(",")
        if tokens[0] == 'C' and tokens[1] == 'start-algo':
            print("starting-algo")
            self.active = True
            return self.start()
        if not self.active:
            return []
        return []
    def start(self):
        return [{"type": "limit",
                 "side": "bid",
                 "quantity": 10000,
                 "price": Decimal(1.0 ),
                 "trade_id" : "ME"}]

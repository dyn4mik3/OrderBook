from decimal import Decimal

class Algorithm(object):
    def __init__(self, order_book):
        self.active = False
        self.order_book = order_book
        self.volume = 0
        self.my_volume = 0

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
                 "price": Decimal(1.04 ),
                 "trade_id" : "ME"}]

    def trade_stats(self, trade):
        for i in trade:
            self.volume += i['quantity']
            if i['party1'][0] == "ME" or \
               i['party2'][0] == "ME":
                self.my_volume += i['quantity']
    def stats(self):
        if (self.volume > 0):
            return (self.volume, self.my_volume,
                    self.my_volume / self.volume)
        else:
            return None

from decimal import * 
import time, random
from order import Order
from orderlist import OrderList

def random_quote():
    return {'timestamp': time.time(), 'quantity': Decimal(random.randrange(10000))/100, 'price': Decimal(random.randrange(10000))/100,
            'order_id': random.randrange(1,10000), 'trade_id': random.randrange(1,10000)}

print "***Generating 10 random Orders***"
for x in range(0,11):
    print Order(random_quote(), None)

print "***Generating a Test OrderList ***"
order_list = OrderList()
for x in range(0,11):
    order_list.append_order(Order(random_quote(), order_list))
print order_list

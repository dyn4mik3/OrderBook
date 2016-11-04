#!/usr/bin/python

import sys
from orderbook import OrderBook
from six.moves import cStringIO
from builtins import input
from decimal import Decimal
import importlib

if __name__ == '__main__':
    def process_line(order_book, line):
        tokens = line.strip().split(",")
        d = {"type" : "limit",
             "side" : "bid" if tokens[0] == 'B' else 'ask',
             "quantity": int(tokens[1]),
             "price" : Decimal(tokens[2]),
             "trade_id" : trade_id}
        if len(tokens) >=4:
            d['tag'] = tokens[3]
        return order_book.process_order(d, False, False)
                
    
    order_book = OrderBook()
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("usage: %s input.csv [algo]" % sys.argv[0])
        sys.exit(0)
    if len(sys.argv) == 3:
        myalgomodule = importlib.import_module(sys.argv[2])
        myalgo = myalgomodule.Algorithm()
    else:
        myalgo = None
    try:
        reader = open(sys.argv[1], 'r')
        trade_id = 0
        for line in reader:
            trades = None
            order = None
            if line[0] == '#':
                next
            elif line[0] == 'B' or line[0] == 'A':
                (trade, order) = process_line(order_book, line)
                trade_id = trade_id + 1
            # Manual Debugging
            print ("\n")
            print ("Input: " + line)
            print (order_book)

            if myalgo != None:
                algo_orders = myalgo.process_order(line,
                                                   trades, order,
                                                   order_book)
                for line in algo_orders:
                    line['trade_id'] = trade_id
                    (trade, order) = order_book.process_order(line,
                                                              False,
                                                              True)
                    trade_id = trade_id + 1
                if len(algo_orders) > 0:
                    print("\n")
                    print("After algo")
                    print(order_book)

            input("Press enter to continue.")
        reader.close()
    except IOError:
        print ('Cannot open input file "%s"' % sys.argv[1])
        sys.exit(1)

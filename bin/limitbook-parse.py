#!/usr/bin/python

import sys
from orderbook import OrderBook
from six.moves import cStringIO
from builtins import input
from decimal import Decimal

if __name__ == '__main__':
    order_book = OrderBook()
    if len(sys.argv) != 2:
        print("usage: %s input.csv" % sys.argv[0])
        sys.exit(0)
    try:
        reader = open(sys.argv[1], 'r')
        trade_id = 0
        for line in reader:
            if line[0] == 'B' or line[0] == 'A':
                tokens = line.split(",")
                (trades, order) = order_book.process_order(
                    {"type" : "limit",
                     "side" : "bid" if tokens[0] == 'B' else 'ask',
                     "quantity": int(tokens[1]),
                     "price" : Decimal(tokens[2]),
                     "trade_id" : trade_id}, False, False)
                trade_id = trade_id + 1
            # Manual Debugging
            print ("\n")
            print ("Input: " + line)
            print (order_book)
            input("Press enter to continue.")
        reader.close()
    except IOError:
        print ('Cannot open input file "%s"' % sys.argv[1])
        sys.exit(1)

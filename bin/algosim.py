#!/usr/bin/python

import sys
from orderbook import OrderBook
from six.moves import cStringIO
from builtins import input
from decimal import Decimal
from six.moves import cStringIO as StringIO
from six.moves import zip_longest
import importlib
import json
import copy
import difflib
import pprint

d = difflib.Differ()
format='html'

if __name__ == '__main__':
    def printme(*args):
        if format == 'html':
            print(*args)
            print('<br>')
        else:
            print(*args)

    def print_orderbook(newbook, oldbook):
        if format == 'html':
            tempfile = StringIO()
            tempfile.write('<table>')
            tempfile.write('<tr>')
            tempfile.write("<td><b>Bids</b></td>")
            tempfile.write("<td><b>Asks</b></td>")
            tempfile.write("</tr>")
            bids_new = []
            asks_new = []

            bids_old = []
            asks_old = []
            if newbook.bids != None and len(newbook.bids) > 0:
                for key, value in newbook.bids.price_tree.items(reverse=True):
                    for order in value:
                        bids_new += [str(order)]
            if newbook.asks != None and len(newbook.asks) > 0:
                for key, value in list(newbook.asks.price_tree.items()):
                    for order in value:
                        asks_new += [str(order)]
            if oldbook.bids != None and len(oldbook.bids) > 0:
                for key, value in oldbook.bids.price_tree.items(reverse=True):
                    for order in value:
                        bids_old += [str(order)]
            if oldbook.asks != None and len(oldbook.asks) > 0:
                for key, value in list(oldbook.asks.price_tree.items()):
                    for order in value:
                        asks_old += [str(order)]

            bids_diff = list(d.compare(bids_old, bids_new))
            asks_diff = list(d.compare(asks_old, asks_new))
            bids = []
            for i in bids_diff:
                if i[0:2] == '? ':
                    continue
                elif i[0:2] == '+ ':
                    bids += ["<b>" + i[2:] + "</b>"]
                elif i[0:2] == '- ':
                    bids += ["<strike>" + i[2:] + "</strike>"]
                else:
                    bids += [i]

            asks = []
            for i in asks_diff:
                if i[0:2] == '? ':
                    continue
                elif i[0:2] == '+ ':
                    asks += ["<b>" + i[2:] + "</b>"]
                elif i[0:2] == '- ':
                    asks += ["<strike>" + i[2:] + "</strike>"]
                else:
                    asks += [i]
                        
            for i in zip_longest(bids, asks):
                tempfile.write('<tr><td>' + \
                               (i[0] if i[0] is not None else '') + \
                               '</td><td>' + \
                               (i[1] if i[1] is not None else '') + \
                               '</td></tr>\n')
            tempfile.write('</table><p>')
            tempfile.write("\n<b>Trades</b><br>\n")
            if newbook.tape != None and len(newbook.tape) > 0:
                num = 0
                for entry in newbook.tape:
                    if num < 10: # get last 5 entries
                        tempfile.write(str(entry['quantity']) + " @ " + str(entry['price']) + " (" + str(entry['timestamp']) + ") " + str(entry['party1'][0]) + "/" + str(entry['party2'][0]) + "<br>\n")
                        num += 1
                    else:
                        break
            tempfile.write("\n")
            print(tempfile.getvalue())
        else:
            print(newbook)
    
    def process_line(order_book, line, output=True):
        tokens = line.strip().split(",")
        d = {"type" : "limit",
             "side" : "bid" if tokens[0] == 'B' else 'ask',
             "quantity": int(tokens[1]),
             "price" : Decimal(tokens[2]),
             "trade_id" : tokens[3]}
        if output:
            printme('external order=', pprint.pformat(d))
        return order_book.process_order(d, False, False)
                
    
    order_book = OrderBook()
    if len(sys.argv) != 2 and len(sys.argv) != 3 and len(sys.argv) != 4:
        printme("usage: %s input.csv [algo]" % sys.argv[0])
        sys.exit(0)
    if len(sys.argv) == 3:
        myalgomodule = importlib.import_module(sys.argv[2])
        myalgo = myalgomodule.Algorithm(order_book)
    elif len(sys.argv) == 4:
        myalgomodule = importlib.import_module(sys.argv[2])
        json_data=open(sys.argv[3]).read()
        data = json.loads(json_data)
        myalgo = myalgomodule.Algorithm(order_book, **data)
    else:
        myalgo = None
    try:
        reader = open(sys.argv[1], 'r')
        start_algo = False
        for line in reader:
            trades = None
            order = None
            if start_algo:
                printme("--------- START -------")
            old_orderbook = copy.deepcopy(order_book)
            if line[0] == '#':
                next
            elif line[0] == 'B' or line[0] == 'A':
                (trade, order) = process_line(order_book, line, start_algo)
                myalgo.process_trade(trade, 'trade')
            elif line[0:12] == 'C,start-algo':
                start_algo = True
                printme("--------- START -------")

            if not start_algo:
                continue
            # Manual Debugging
            printme ("\n")
            print_orderbook(order_book, old_orderbook)
            stats=myalgo.stats()
            printme ("total volume=", stats[0])
            printme ("my volume=", stats[1])
            printme ("participation=", stats[3])

            if myalgo != None:
                (algo_orders, mode) = myalgo.process_order(line, order)
                printme('')
                printme("RUNNING ALGO WITH MODE=", mode)
                old_orderbook = copy.deepcopy(order_book)
                for line in algo_orders:
                    printme(pprint.pformat(line))
                    if line['type'] == 'cancel':
                        order_book.cancel_order(line['side'],
                                                line['order_id'])
                    elif line['type'] == 'cancel_all':
                        if line['side'] == "bid":
                            q = order_book.bids
                        elif line['size'] == 'ask':
                            q = order_book.asks
                        else:
                            sys.exit('not given bid or ask')
                        for order in q.price_tree.get(Decimal(line['price']),
                                                      []):
                            if order.trade_id == line['trade_id']:
                                order_book.cancel_order(line['side'],
                                                        order.order_id)
                    elif line['type'] == 'modify':
                        order_book.modify_order(line['order_id'], {
                            'side': line['side'],
                            'price': line['price'],
                            'quantity': line['quantity']})
                    else:
                        (trade, order) = order_book.process_order(line,
                                                                  False,
                                                                  False)
                        myalgo.process_trade(trade, mode)
                if len(algo_orders) > 0:
                    printme("\n")
                    printme("After algo")
                    print_orderbook(order_book, old_orderbook)
                    stats=myalgo.stats()
                    printme ("total volume=", stats[0])
                    printme ("my volume=", stats[1])
                    printme ("participation=", stats[3])
                else:
                    printme("No action by algo")
                printme("--------- END -------")
        reader.close()
    except IOError:
        printme ('Cannot open input file "%s"' % sys.argv[1])
        sys.exit(1)

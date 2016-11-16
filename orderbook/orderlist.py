class OrderList(object):
    '''
    A doubly linked list of Orders. Used to iterate through Orders when
    a price match is found. Each OrderList is associated with a single
    price. Since a single price match can have more quantity than a single 
    Order, we may need multiple Orders to fullfill a transaction. The
    OrderList makes this easy to do. OrderList is naturally arranged by time.
    Orders at the front of the list have priority.
    '''

    def __init__(self):
        self.head_order = None # first order in the list
        self.tail_order = None # last order in the list
        self.length = 0 # number of Orders in the list
        self.volume = 0 # sum of Order quantity in the list AKA share volume
        self.last = None # helper for iterating 

    def __len__(self):
        return self.length

    def __iter__(self):
        self.last = self.head_order
        return self

    def next(self):
        '''Get the next order in the list. 
        
        Set self.last as the next order. If there is no next order, stop
        iterating through list.
        '''
        if self.last == None:
            raise StopIteration
        else:
            return_value = self.last
            self.last = self.last.next_order
            return return_value

    __next__ = next # python3

    def get_head_order(self):
        return self.head_order

    def append_order(self, order):
        if len(self) == 0:
            order.next_order = None
            order.prev_order = None
            self.head_order = order
            self.tail_order = order
        else:
            order.prev_order = self.tail_order
            order.next_order = None
            self.tail_order.next_order = order
            self.tail_order = order
        self.length +=1
        self.volume += order.quantity

    def remove_order(self, order):
        self.volume -= order.quantity
        self.length -= 1
        if len(self) == 0: # if there are no more Orders, stop/return
            return
        
        # Remove an Order from the OrderList. First grab next / prev order
        # from the Order we are removing. Then relink everything. Finally
        # remove the Order.
        next_order = order.next_order
        prev_order = order.prev_order
        if next_order != None and prev_order != None:
            next_order.prev_order = prev_order
            prev_order.next_order = next_order
        elif next_order != None: # There is no previous order
            next_order.prev_order = None
            self.head_order = next_order # The next order becomes the first order in the OrderList after this Order is removed
        elif prev_order != None: # There is no next order
            prev_order.next_order = None
            self.tail_order = prev_order # The previous order becomes the last order in the OrderList after this Order is removed

    def move_to_tail(self, order):
        '''After updating the quantity of an existing Order, move it to the tail of the OrderList

        Check to see that the quantity is larger than existing, update the quantities, then move to tail.
        '''
        if order.prev_order != None: # This Order is not the first Order in the OrderList
            order.prev_order.next_order = order.next_order # Link the previous Order to the next Order, then move the Order to tail
        else: # This Order is the first Order in the OrderList
            self.head_order = order.next_order # Make next order the first

        order.next_order.prev_order = order.prev_order

        # Move Order to the last position. Link up the previous last position Order.
        self.tail_order.next_order = order
        self.tail_order = order

    def __str__(self):
        from six.moves import cStringIO as StringIO
        temp_file = StringIO()
        for order in self:
            temp_file.write("%s\n" % str(order))
        #temp_file.write("%s\n" % str(self.head_order))
        return temp_file.getvalue()
            

            


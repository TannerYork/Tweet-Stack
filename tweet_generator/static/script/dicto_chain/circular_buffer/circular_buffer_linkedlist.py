#!python

from __future__ import division, print_function  # Python 2 and 3 compatibility

class Node():
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularBufferLinkedList():
    def __init__(self, size):
        self.size = size # max size of the queue
        self.length = 0 # items in queue
        self.head = None # head node of queue
        self.tail = None # tail node of queue

    def enqueue(self, item):
        """ Add an item to the end of the queue """
        node = Node(item)

        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
            self.length += 1
            if self.length >= self.size:
                self.dequeue()
                self.length -= 1

    def dequeue(self):
        """ Remove oldest item in queue """
        if self.head is None:
            raise KeyError('No elements found to dequeue.')
        self.head = self.head.next

    def current_items(self):
        """ Returns an array of the current items in queue """
        items = []
        node = self.head
        while node is not None:
            items.append(node.data)
            node = node.next
        return items

def test_queue():
    queue = LinkedListQueue(3)
    assert queue.size == 3
    
    # Test enqueue 
    queue.enqueue('I')
    assert queue.head.data == 'I'
    queue.enqueue('like')
    assert queue.head.next.data == 'like'
    assert queue.tail.data == 'like'
    queue.enqueue('pie')
    assert queue.tail.data == 'pie'

    # Test enqueue and dequeue
    queue.enqueue('and')
    assert queue.head.data == 'like'
    assert queue.tail.data == 'and'

    # Test current_items
    items = queue.current_items()
    assert items == ['like', 'pie', 'and']
    print(items)
    print('All test pased with OK')

if __name__ == '__main__':
    test_queue()


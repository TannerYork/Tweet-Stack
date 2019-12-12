#!python

class CircularBuffer(list):
    def __init__(self, size):
        super(CircularBuffer, self).__init__()
        self.size = size
        for _ in range(0, size): 
            self.append(None)

    def enqueue(self, item):
        self.pop(0)
        self.append(item)
        
def main():
    circular_buffer = CircularBuffer(2)
    fish_words = ['one', 'fish', 'two', 'fish', 'red', 'fish', 'blue', 'fish']
    # Test enqueue
    for word in fish_words:
        print(circular_buffer)
        circular_buffer.enqueue(word)
   
if __name__ == '__main__':
    main()
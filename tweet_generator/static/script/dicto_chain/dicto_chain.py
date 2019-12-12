#!python

from __future__ import division, print_function  # Python 2 and 3 compatibility
from tweet_generator.static.script.dicto_chain.dictogram.dictogram import Dictogram
from tweet_generator.static.script.dicto_chain.circular_buffer.circular_buffer import CircularBuffer
import random
import math
import re

START_TOKEN = '*START'
STOP_TOKEN = '*STOP'

class DictovChain(dict):
    """Markov Chain implemented as a subclass of the dictionary type"""

    def __init__(self, words_list, order=2):
        """Initialize the markov chain as a new dict with a list of words"""
        super(DictovChain, self).__init__()
        self.start_tokens = Dictogram()
        self.order = int(order)
        
        circular_buffer = CircularBuffer(int(order))
        prev_words = None
        for word in words_list:
            prev_words = list(circular_buffer)
            circular_buffer.enqueue(word)
            if circular_buffer[0] is not None:
                if prev_words[0] is None: prev_words[0] = START_TOKEN
                self.add_count(' '.join(circular_buffer), ' '.join(prev_words))

    def add_count(self, words, prev_words, count=1):
        """Add next word to words chain by the count amount"""
        if prev_words not in self:
            self[prev_words] = Dictogram([words])
        else:
            self[prev_words].add_count(words, count)
        if START_TOKEN in prev_words:
            self.start_tokens.add_count(words)

    def sample(self, dictogram):
        """Returns a random word from the histogram based on the probabilistic distribution of each word"""
        total = sum(dictogram.values()) 
        randint = random.randint(1, total)
        for word in dictogram:
            if randint-dictogram[word] <= 0:
                return word
            randint -= dictogram[word]

    def walk(self, count):
        """Perform a random walk on the chain as long as the count"""
        curr_words = self.sample(self.start_tokens)
        sentence = list(re.sub(START_TOKEN, '', curr_words).strip())
        for _ in range(1, count):
            if curr_words not in self:
                return ' '.join(sentence)
            curr_words = self.sample(self[curr_words])
            curr_word = curr_words[self.order-1]
            sentence.append(curr_words)
        return ' '.join(sentence)

if __name__ == '__main__':
    fish_words = ['one', 'fish', 'two', 'fish', 'red', 'fish', 'blue', 'fish', 'red', 'fish', 'green', 'fish', 'two', 'fish', 'blue', 'fish']
    markov_chain = DictovChain(fish_words)
    print(markov_chain)
    print(markov_chain.start_tokens)
    print(markov_chain.walk(20))
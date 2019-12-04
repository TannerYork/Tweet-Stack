#!python

from __future__ import division, print_function  # Python 2 and 3 compatibility
from tweet_generator.static.script.dicto_chain.dictogram.dictogram import Dictogram
import random
import math


class DictoChain(dict):
    """Markov Chain implemented as a subclass of the dictionary type"""

    def __init__(self, words_list=None, order=2):
        """Initialize the markov chain as a new dict with a list of words"""
        super(DictoChain, self).__init__()
        self.start_tokens = Dictogram()
        self.order = int(order)

        for index, word in enumerate(words_list):
            if index+self.order < len(words_list):
                words = words_list[index:index+self.order]
                next_words = words_list[index+(self.order-1):index+((2*self.order)-1)]
                self.add_count(words, next_words)
            else:
                words = words_list[index:index+self.order]
                self.add_count(words)

    def add_count(self, words, next_words=None, count=1):
        """Add next word to words chain by the count amount"""
        words = ' '.join(words)
        if next_words is not None:
            next_words = ' '.join(next_words)

        if words not in self:
            self[words] = Dictogram([next_words])
        elif next_words is not None:
            self[words].add_count(next_words, count)

        if '.' in words and next_words is not None and '.' not in next_words:
            self.start_tokens.add_count(next_words)


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
        sentence = [curr_words]
        for _ in range(1, count):
            if None in self.data[curr_words]:
                return ' '.join(sentence)
            curr_words = self.sample(self.data[curr_words])
            curr_word = curr_words.split(' ')[self.order-1]
            sentence.append(curr_word)
        return ' '.join(sentence)

if __name__ == '__main__':
    fish_words = ['one', 'fish', 'two', 'fish.', 'red', 'fish', 'blue', 'fish', 'one', 'fish', 'two', 'fish.', 'one', 'fish', 'two', 'fish.']
    markov_chain = DictoChain(fish_words)
    print(markov_chain)
    print(markov_chain.start_tokens)
    print(markov_chain.walk(20))
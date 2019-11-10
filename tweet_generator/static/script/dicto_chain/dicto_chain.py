#!python

from __future__ import division, print_function  # Python 2 and 3 compatibility
from tweet_generator.static.script.dicto_chain.dictogram.dictogram import Dictogram
import random
import math


class DictoChain(dict):
    """Markov Chain implemented as a subclass of the dictionary type"""

    def __init__(self, words_list=None):
        """Initialize the markov chain as a new dict with a list of words"""
        super(DictoChain, self).__init__()
        self.dictogram = Dictogram(words_list)

        for index, word in enumerate(words_list):
            if index+1 < len(words_list):
                self.add_word(word, words_list[index+1])
            else:
                self.add_word(word)

    def add_word(self, word, next_word=None, count=1):
        """Add next word to words chain by the count amount"""
        
        if next_word is None:
            pass
        elif word not in self:
            self[word] = Dictogram([next_word])
        elif next_word not in self[word]:
            self[word].add_count(next_word, count)
        elif next_word in self[word]:
            self[word].add_count(next_word, count)

    def walk(self, count):
        """Perform a random walk on the chain as long as the count"""
        curr_word = self.dictogram.sample()
        sentence = [curr_word]
        for i in range(1, count):
            curr_word = self[curr_word].sample()
            sentence.append(curr_word)
        return ' '.join(sentence) + '.'


if __name__ == '__main__':
    fish_words = ['one', 'fish', 'two', 'fish', 'red', 'fish', 'blue', 'fish']
    markov_chain = DictoChain(fish_words)
    print(markov_chain)
from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify  
from django.db import models
import random
import re

STOP_TOKEN = '*STOP'
START_TOKEN = '*START'

class MarkovChain(models.Model):
    name = models.CharField(max_length=200)
    data = JSONField(default=dict)
    start_tokens = JSONField(default=dict)
    order = models.IntegerField(default=1)
    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.name

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
        sentence = [re.sub('\*START', '', curr_words).strip()]
        while STOP_TOKEN not in curr_words:
            curr_words = self.sample(self.data[curr_words])
            curr_word = curr_words.split(' ')[self.order-1]
            sentence.append(curr_word)
        sentence.pop()
        return ' '.join(sentence)

    def save(self, *args, **kwargs):
        """ Creates a URL safe slug automatically when a new chain is created. """
        if not self.pk:
            self.slug = slugify(self.name)
        return super(MarkovChain, self).save(*args, **kwargs)
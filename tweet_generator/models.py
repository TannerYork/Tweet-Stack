from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify  
from django.db import models
import random


class MarkovChain(models.Model):
    name = models.CharField(max_length=200)
    data = JSONField(default=dict)
    dictogram = JSONField(default=dict)
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
        curr_word = self.sample(self.dictogram)
        sentence = [curr_word]
        for i in range(1, count):
            curr_word = self.sample(self.data[curr_word])
            sentence.append(curr_word)
        return ' '.join(sentence) + '.'

    def save(self, *args, **kwargs):
        """ Creates a URL safe slug automatically when a new chain is created. """
        if not self.pk:
            self.slug = slugify(self.name)
        return super(MarkovChain, self).save(*args, **kwargs)
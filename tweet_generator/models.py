from django.contrib.postgres.fields import HStoreField, JSONField
from django.db import models


class Generator(models.Model):
    name = models.CharField(max_length=200)
    data = JSONField()

    def __str__(self):
        return self.name
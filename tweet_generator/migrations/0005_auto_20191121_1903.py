# Generated by Django 2.2.6 on 2019-11-21 19:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_generator', '0004_markovchain_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='markovchain',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='markovchain',
            name='dictogram',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='markovchain',
            name='slug',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]

# Generated by Django 2.2.6 on 2019-11-21 05:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_generator', '0002_auto_20191114_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='markovchain',
            name='dictogram',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]
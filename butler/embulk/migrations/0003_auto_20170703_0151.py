# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embulk', '0002_columnoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='columnoption',
            name='timestamp_format',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='columnoption',
            name='type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='columnoption',
            name='value_type',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

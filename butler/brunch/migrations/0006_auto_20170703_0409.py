# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 22:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brunch', '0005_databaseconfig_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='databaseconfig',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='databaseconfig',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

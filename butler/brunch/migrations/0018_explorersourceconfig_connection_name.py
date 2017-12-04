# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-07 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brunch', '0017_auto_20170704_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='explorersourceconfig',
            name='connection_name',
            field=models.CharField(choices=[(b'default', b'default'), (b'qa', b'qa'), (b'replica', b'replica'), (b'redshift', b'redshift')], default='replica', max_length=50),
            preserve_default=False,
        ),
    ]
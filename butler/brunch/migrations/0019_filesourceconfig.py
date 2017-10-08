# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-07 21:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brunch', '0018_explorersourceconfig_connection_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileSourceConfig',
            fields=[
                ('sourceconfig_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='brunch.SourceConfig')),
                ('file', models.FileField(upload_to='FileSourceConfig/')),
            ],
            options={
                'abstract': False,
            },
            bases=('brunch.sourceconfig',),
        ),
    ]

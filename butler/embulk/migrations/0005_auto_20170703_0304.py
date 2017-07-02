# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 21:34
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import embulk.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('embulk', '0004_auto_20170703_0234'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseColumnOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Column name(s) used in select', max_length=255)),
                ('value_type', models.CharField(blank=True, choices=[(b'long', 'long'), (b'double', 'double'), (b'float', 'float'), (b'decimal', 'decimal'), (b'boolean', 'boolean'), (b'string', 'string'), (b'json', 'json'), (b'date', 'date'), (b'time', 'time'), (b'timestamp', 'timestamp')], max_length=50, verbose_name='Cast as')),
                ('type', models.CharField(blank=True, choices=[(b'boolean', 'boolean'), (b'long', 'long'), (b'double', 'double'), (b'string', 'string'), (b'json', 'json'), (b'timestamp', 'timestamp')], max_length=50, verbose_name='Convert to')),
                ('timestamp_format', models.CharField(blank=True, help_text='default : %Y-%m-%d for date, %H:%M:%S for time, %Y-%m-%d %H:%M:%S for timestamp', max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(embulk.models.AbstractBaseModel, models.Model),
        ),
        migrations.CreateModel(
            name='DatabaseConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('connection_name', models.CharField(choices=[(b'default', b'default'), (b'qa', b'qa'), (b'replica', b'replica'), (b'redshift', b'redshift')], max_length=50)),
                ('select', models.CharField(max_length=1024)),
                ('table', models.CharField(max_length=128)),
                ('where', models.CharField(blank=True, max_length=1024)),
                ('batch_size', models.IntegerField(default=10000)),
                ('incremental_columns', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, help_text='Column name(s) used in select', size=None)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='embulk_databaseconfig_created', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='embulk_databaseconfig_last_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(embulk.models.AbstractBaseModel, models.Model),
        ),
        migrations.RemoveField(
            model_name='columnoption',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='columnoption',
            name='editor',
        ),
        migrations.RemoveField(
            model_name='config',
            name='column_options',
        ),
        migrations.RemoveField(
            model_name='config',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='config',
            name='default_column_options',
        ),
        migrations.RemoveField(
            model_name='config',
            name='editor',
        ),
        migrations.DeleteModel(
            name='ColumnOption',
        ),
        migrations.DeleteModel(
            name='Config',
        ),
        migrations.AddField(
            model_name='databasecolumnoption',
            name='config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='embulk.DatabaseConfig'),
        ),
        migrations.AddField(
            model_name='databasecolumnoption',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='embulk_databasecolumnoption_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='databasecolumnoption',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='embulk_databasecolumnoption_last_modified', to=settings.AUTH_USER_MODEL),
        ),
    ]
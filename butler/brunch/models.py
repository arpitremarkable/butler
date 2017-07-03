# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.db import models
from django_celery_beat.models import PeriodicTask

from brunch.utils import to_namedtuple


# Create your models here.


class AbstractBaseModel(object):

    def __unicode__(self):
        try:
            return self.name
        except AttributeError:
            try:
                return self.title
            except AttributeError:
                return ''


class BaseModel(AbstractBaseModel, models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseAuthorModel(BaseModel):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, related_name='%(app_label)s_%(class)s_created')
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, related_name='%(app_label)s_%(class)s_last_modified')

    class Meta:
        abstract = True


class Config(BaseAuthorModel):
    pass


class DatabaseConfig(Config):
    name = models.CharField(max_length=255, unique=True)
    connection_name = models.CharField(
        max_length=50, blank=False, choices=to_namedtuple(settings.DATABASES.keys()).__dict__.items()
    )
    select = models.CharField(max_length=1024, blank=False)
    table = models.CharField(max_length=128, blank=False)
    where = models.CharField(max_length=1024, blank=True)
    batch_size = models.IntegerField(blank=False, default=10000)
    incremental_columns = pg_fields.ArrayField(
        models.CharField(max_length=50), default=list, blank=True, help_text='Column name(s) used in select'
    )


class DatabaseColumnOption(BaseAuthorModel):
    value_types = to_namedtuple(('long', 'double', 'float', 'decimal', 'boolean', 'string', 'json', 'date', 'time', 'timestamp', ))
    types = to_namedtuple(('boolean', 'long', 'double', 'string', 'json', 'timestamp', ))

    config = models.ForeignKey(DatabaseConfig)
    name = models.CharField(max_length=255, help_text='Column name(s) used in select')
    value_type = models.CharField(blank=True, max_length=50, verbose_name='Cast as', choices=value_types.__dict__.items())
    type = models.CharField(blank=True, max_length=50, verbose_name='Convert to', choices=types.__dict__.items())
    timestamp_format = models.CharField(
        blank=True, max_length=50, help_text='default : %Y-%m-%d for date, %H:%M:%S for time, %Y-%m-%d %H:%M:%S for timestamp'
    )


class ScheduledTask(PeriodicTask):
    config = models.OneToOneField(Config)

    def save(self, *args, **kwargs):
        import json
        from brunch.tasks import execute_config
        self.name = self.config.name
        self.task = "%s.%s" % (execute_config.__module__, execute_config.__name__)
        self.kwargs = json.dumps({
            'config_id': self.config.id,
        })
        superb = super(ScheduledTask, self).save(*args, **kwargs)
        # PeriodicTask.save(self, *args, **kwargs)
        self.periodictask_ptr.save()
        return superb

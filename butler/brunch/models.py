# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_on = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-modified_on']


class BaseAuthorModel(BaseModel):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, related_name='%(app_label)s_%(class)s_created')
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, related_name='%(app_label)s_%(class)s_last_modified')

    class Meta(BaseModel.Meta):
        abstract = True


class GenericBaseModel(BaseAuthorModel):
    important_info = ()
    _content_type = models.ForeignKey(ContentType)
    special_object = GenericForeignKey('_content_type', 'id')

    def save(self, *args, **kwargs):
        self.special_object = self
        return super(GenericBaseModel, self).save(*args, **kwargs)

    class Meta(BaseAuthorModel.Meta):
        abstract = True

    def get_important_info(self):
        info = {'table', 'connection_name', 'mode', 'NATURE', }
        return info.union(set(self.special_object.important_info))

    def __unicode__(self):
        important_info = self.get_important_info()
        msg = []
        for info in important_info:
            if hasattr(self.special_object, info):
                msg.append("%(info_lower)s: %%(%(info)s)s" % {'info_lower': info.lower(), 'info': info} % {
                    info: getattr(self.special_object, info)
                })
        return ', '.join(msg) or super(GenericBaseModel, self).__unicode__()


class Config(GenericBaseModel):
    NATURE = 'generic'
    name = models.CharField(max_length=255)


class SourceConfig(Config):
    pass


class TargetConfig(Config):
    pass


class DatabaseSourceConfig(SourceConfig):
    NATURE = 'database'
    connection_names = to_namedtuple(settings.DATABASES.keys())

    connection_name = models.CharField(
        max_length=50, blank=False, choices=connection_names.__dict__.items()
    )
    select = models.CharField(max_length=1024, blank=False)
    table = models.CharField(max_length=128, blank=False)
    where = models.CharField(max_length=1024, blank=True)
    order_by = models.CharField(max_length=128, blank=True)
    batch_size = models.IntegerField(blank=False, default=10000)
    incremental_columns = pg_fields.ArrayField(
        models.CharField(max_length=50), default=list, blank=True, help_text='Column name(s) used in select'
    )


class ExplorerSourceConfig(SourceConfig):
    NATURE = 'explorer'
    important_info = ('name', )
    query = models.OneToOneField('explorer.Query')
    batch_size = models.IntegerField(blank=False, default=10000)
    connection_name = models.CharField(
        max_length=50, blank=False, choices=to_namedtuple(settings.DATABASES.keys()).__dict__.items()
    )


class FileSourceConfig(SourceConfig):
    NATURE = 'file'
    important_info = ('name', )
    file = models.FileField(upload_to='FileSourceConfig/')


class DatabaseTargetConfig(TargetConfig):
    NATURE = 'database'
    modes = to_namedtuple(('insert', 'insert_direct', 'truncate_insert', 'replace', 'merge', ))

    connection_name = models.CharField(
        max_length=50, blank=False, choices=to_namedtuple(settings.DATABASES.keys()).__dict__.items()
    )
    table = models.CharField(max_length=128, blank=False)
    mode = models.CharField(
        max_length=50, blank=False, choices=modes.__dict__.items()
    )
    merge_keys = pg_fields.ArrayField(
        models.CharField(max_length=50), default=list, blank=True,
        help_text='If merge mode is selected, Column name(s) used in select',
    )


class DatabaseColumnOption(BaseAuthorModel):
    value_types = to_namedtuple(('long', 'double', 'float', 'decimal', 'boolean', 'string', 'json', 'date', 'time', 'timestamp', ))
    types = to_namedtuple(('boolean', 'long', 'double', 'string', 'json', 'timestamp', ))

    config = models.ForeignKey(Config, related_name='column_options')
    name = models.CharField(max_length=255, help_text='Column name(s) used in select')
    value_type = models.CharField(blank=True, max_length=50, verbose_name='Cast as', choices=value_types.__dict__.items())
    type = models.CharField(blank=True, max_length=50, verbose_name='Convert to', choices=types.__dict__.items())
    timestamp_format = models.CharField(
        blank=True, max_length=50, help_text='default : %Y-%m-%d for date, %H:%M:%S for time, %Y-%m-%d %H:%M:%S for timestamp'
    )


class ScheduledTask(BaseAuthorModel, PeriodicTask):
    source_config = models.ForeignKey(SourceConfig)
    target_config = models.ForeignKey(TargetConfig)

    def run(self):
        from brunch import tasks
        tasks.unbound_execute_config.delay(scheduled_task_id=self.id)

    def get_latest_log(self):
        log_content = {}
        try:
            with open(os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_task_%d.stdout' % self.id), 'r') as f:
                log_content['info'] = f.read()
        except IOError:
            log_content['info'] = ''
        try:
            with open(os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_task_%d.stderr' % self.id), 'r') as f:
                log_content['error'] = f.read()
        except IOError:
            log_content['error'] = ''
        return log_content

    def save(self, *args, **kwargs):
        import json
        from brunch.tasks import execute_config
        superb = super(ScheduledTask, self).save(*args, **kwargs)
        self.name = "%s -> %s" % (
            self.source_config.special_object, self.target_config.special_object
        )
        self.task = "%s.%s" % (execute_config.__module__, execute_config.__name__)
        self.kwargs = json.dumps({
            'scheduled_task_id': self.id,
        })
        self.periodictask_ptr.save()
        return superb

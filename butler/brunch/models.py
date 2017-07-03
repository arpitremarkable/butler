# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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


class GenericBaseModel(BaseAuthorModel):
    _content_type = models.ForeignKey(ContentType)
    special_object = GenericForeignKey('_content_type', 'id')

    def save(self, *args, **kwargs):
        self.special_object = self
        return super(GenericBaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Config(GenericBaseModel):
    name = models.CharField(max_length=255, unique=True)

    @staticmethod
    def __new__(cls, *args, **kwargs):
        kwargs['use_class'] = kwargs['use_class'] if 'use_class' in kwargs else Config
        if not issubclass(cls, kwargs['use_class']):
            return super(kwargs['use_class'], cls).__new__(cls, *args, **kwargs)
        model = cls

        def fields():
            return (f for f in cls._meta.concrete_fields)

        for i, field in enumerate(fields()):
            if getattr(field, 'related_model', None) is ContentType:
                # db to py object
                try:
                    _content_type_id = args[i]
                    if _content_type_id is models.base.DEFERRED:
                        break
                    _content_type = ContentType._default_manager.get(pk=_content_type_id)
                except ContentType.DoesNotExist:
                    break
                except IndexError:
                    try:
                        _content_type = kwargs[field.name]
                    except KeyError:
                        try:
                            _content_type = kwargs[field.attname]
                            if _content_type_id is models.base.DEFERRED:
                                break
                            _content_type = ContentType._default_manager.get(
                                pk=_content_type_id
                            )
                        except (KeyError, ContentType.DoesNotExist):
                            break
                model = _content_type.model_class()
                break
        use_class = kwargs.pop('use_class')
        return super(use_class, cls).__new__(model, *args, **kwargs)


class SourceConfig(Config):
    pass


class TargetConfig(Config):
    pass


class DatabaseSourceConfig(SourceConfig):
    connection_names = to_namedtuple(settings.DATABASES.keys())

    connection_name = models.CharField(
        max_length=50, blank=False, choices=connection_names.__dict__.items()
    )
    select = models.CharField(max_length=1024, blank=False)
    table = models.CharField(max_length=128, blank=False)
    where = models.CharField(max_length=1024, blank=True)
    batch_size = models.IntegerField(blank=False, default=10000)
    incremental_columns = pg_fields.ArrayField(
        models.CharField(max_length=50), default=list, blank=True, help_text='Column name(s) used in select'
    )

    def __unicode__(self):
        return "%s:%s (%s)" % (self.connection_name, self.table, self.name)


class DatabaseTargetConfig(TargetConfig):
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

    def __unicode__(self):
        return "%s:%s (%s)" % (self.connection_name, self.table, self.name)


class DatabaseColumnOption(BaseAuthorModel):
    value_types = to_namedtuple(('long', 'double', 'float', 'decimal', 'boolean', 'string', 'json', 'date', 'time', 'timestamp', ))
    types = to_namedtuple(('boolean', 'long', 'double', 'string', 'json', 'timestamp', ))

    config = models.ForeignKey(Config)
    name = models.CharField(max_length=255, help_text='Column name(s) used in select')
    value_type = models.CharField(blank=True, max_length=50, verbose_name='Cast as', choices=value_types.__dict__.items())
    type = models.CharField(blank=True, max_length=50, verbose_name='Convert to', choices=types.__dict__.items())
    timestamp_format = models.CharField(
        blank=True, max_length=50, help_text='default : %Y-%m-%d for date, %H:%M:%S for time, %Y-%m-%d %H:%M:%S for timestamp'
    )


class ScheduledTask(BaseAuthorModel, PeriodicTask):
    source_config = models.ForeignKey(SourceConfig)
    target_config = models.ForeignKey(TargetConfig)

    def save(self, *args, **kwargs):
        import json
        from brunch.tasks import execute_config
        self.name = "%s -> %s" % (
            self.source_config, self.target_config
        )
        self.task = "%s.%s" % (execute_config.__module__, execute_config.__name__)
        self.kwargs = json.dumps({
            'source_config_id': self.source_config.id,
            'target_config_id': self.target_config.id,
        })
        superb = super(ScheduledTask, self).save(*args, **kwargs)
        self.periodictask_ptr.save()
        return superb

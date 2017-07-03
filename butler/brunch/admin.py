# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from brunch.forms import DatabaseColumnOptionModelForm, DatabaseConfigModelForm
from brunch.models import DatabaseColumnOption, DatabaseConfig, ScheduledTask


class DatabaseColumnOptionInlineForm(admin.TabularInline):
    form = DatabaseColumnOptionModelForm
    model = DatabaseColumnOption


class ScheduledTaskInlineForm(admin.TabularInline):
    model = ScheduledTask
    fields = ('interval', 'enabled', )


class DatabaseConfigAdmin(admin.ModelAdmin):
    form = DatabaseConfigModelForm
    inlines = [
        DatabaseColumnOptionInlineForm,
        ScheduledTaskInlineForm,
    ]
    list_display = ('__unicode__', 'last_run_at', 'total_run_count', )

    def last_run_at(self, instance):
        return instance.scheduledtask.last_run_at

    def total_run_count(self, instance):
        return instance.scheduledtask.total_run_count

    def save_model(self, request, obj, *args, **kwargs):
        return super(DatabaseConfigAdmin, self).save_model(request, obj, *args, **kwargs)


admin.site.register(DatabaseConfig, DatabaseConfigAdmin)

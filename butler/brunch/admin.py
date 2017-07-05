# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from brunch.forms import BaseModelForm
from brunch.models import (DatabaseColumnOption, DatabaseSourceConfig,
                           DatabaseTargetConfig, ExplorerSourceConfig,
                           ScheduledTask)


class DatabaseColumnOptionInlineForm(admin.TabularInline):
    form = BaseModelForm
    model = DatabaseColumnOption


class ScheduledTaskInlineForm(admin.ModelAdmin):
    form = BaseModelForm
    model = ScheduledTask
    fields = ('source_config', 'target_config', 'interval', 'enabled', 'crontab', )
    list_display = ('__unicode__', 'last_run_at', 'total_run_count', 'interval', 'enabled', 'crontab', )


class ConfigAdmin(admin.ModelAdmin):
    form = BaseModelForm
    inlines = [
        DatabaseColumnOptionInlineForm,
    ]


admin.site.register(DatabaseSourceConfig, ConfigAdmin)
admin.site.register(DatabaseTargetConfig, ConfigAdmin)
admin.site.register(ExplorerSourceConfig, ConfigAdmin)
admin.site.register(ScheduledTask, ScheduledTaskInlineForm)

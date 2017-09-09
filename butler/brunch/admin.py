# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib import admin, messages
from django.utils.safestring import mark_safe

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
    list_editable = ('interval', )
    actions = ('force_run', 'show_log', )

    def force_run(self, request, queryset):
        for task in queryset:
            task.run()
            messages.success(request, 'Run started for %s' % (task, ))
    force_run.short_description = "Force run selected tasks"

    def show_log(self, request, queryset):
        for task in queryset:
            log_content = task.get_latest_log()
            messages.info(request, mark_safe("""
                %s
                <pre>%s</pre>
            """ % (task, log_content, )))
    show_log.short_description = "Show latest log for selected tasks"


class ConfigAdmin(admin.ModelAdmin):
    form = BaseModelForm
    inlines = [
        DatabaseColumnOptionInlineForm,
    ]


admin.site.register(DatabaseSourceConfig, ConfigAdmin)
admin.site.register(DatabaseTargetConfig, ConfigAdmin)
admin.site.register(ExplorerSourceConfig, ConfigAdmin)
admin.site.register(ScheduledTask, ScheduledTaskInlineForm)

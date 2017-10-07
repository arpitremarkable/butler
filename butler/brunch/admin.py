# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from brunch.forms import BaseModelForm
from brunch.models import (DatabaseColumnOption, DatabaseSourceConfig,
                           DatabaseTargetConfig, ExplorerSourceConfig,
                           ScheduledTask)


class DatabaseColumnOptionInlineForm(admin.TabularInline):
    form = BaseModelForm
    model = DatabaseColumnOption


class ScheduledTaskForm(admin.ModelAdmin):
    form = BaseModelForm
    model = ScheduledTask
    fields = ('source_config', 'target_config', 'interval', 'enabled', 'crontab', )
    list_display = (
        '__unicode__', 'last_run_at', 'total_run_count', 'interval', 'enabled', 'crontab',
        'source_details', 'target_details',
    )
    list_editable = ('interval', )
    actions = ('force_run', 'show_log', )

    def source_details(self, instance):
        return self._config_detail(instance.source_config)

    def target_details(self, instance):
        return self._config_detail(instance.target_config)

    def _config_detail(self, config):
        return mark_safe('<br/>'.join(("%s" % (
            config,
        )).split(',') + [self._config_link(config)]))

    def _config_link(self, config):
        return '<a href="%s">Edit</a>' % (
            reverse("admin:%s_%s_change" % (self.opts.app_label, config.special_object._meta.model_name), args=(config.pk,)),

        )

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


class ExplorerConfigAdmin(ConfigAdmin):
    readonly_fields = ('sql', )
    exclude = ('name', 'creator', 'editor', '_content_type')

    def save_model(self, request, obj, form, change):
        obj.name = form.cleaned_data['query'].__unicode__()
        return super(ExplorerConfigAdmin, self).save_model(request, obj, form, change)

    def sql(self, instance):
        return mark_safe("<pre>%s</pre>" % instance.query.sql)


admin.site.register(DatabaseSourceConfig, ConfigAdmin)
admin.site.register(DatabaseTargetConfig, ConfigAdmin)
admin.site.register(ExplorerSourceConfig, ExplorerConfigAdmin)
admin.site.register(ScheduledTask, ScheduledTaskForm)

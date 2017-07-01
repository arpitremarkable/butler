# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from brunch.models import ExplorerSource


class ExplorerSourceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'link', )
    list_display_links = ('__unicode__', 'link', )
    list_select_related = ('query', )
    list_filter = ('query__title',)
    fields = ('query', )

    def link(self, instance):
        return '<a href="%s" target="_blank">open</a>' % (instance.query.get_absolute_url(), )
    link.allow_tags = True


admin.site.register(ExplorerSource, ExplorerSourceAdmin)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from embulk.forms import DatabaseColumnOptionModelForm, DatabaseConfigModelForm
from embulk.models import DatabaseColumnOption, DatabaseConfig


class DatabaseColumnOptionInlineForm(admin.TabularInline):
    form = DatabaseColumnOptionModelForm
    model = DatabaseColumnOption


class DatabaseConfigAdmin(admin.ModelAdmin):
    form = DatabaseConfigModelForm
    inlines = [
        DatabaseColumnOptionInlineForm,
    ]


admin.site.register(DatabaseConfig, DatabaseConfigAdmin)

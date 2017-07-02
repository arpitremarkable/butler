# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from brunch.forms import DatabaseColumnOptionModelForm, DatabaseConfigModelForm
from brunch.models import DatabaseColumnOption, DatabaseConfig


class DatabaseColumnOptionInlineForm(admin.TabularInline):
    form = DatabaseColumnOptionModelForm
    model = DatabaseColumnOption


class DatabaseConfigAdmin(admin.ModelAdmin):
    form = DatabaseConfigModelForm
    inlines = [
        DatabaseColumnOptionInlineForm,
    ]


admin.site.register(DatabaseConfig, DatabaseConfigAdmin)

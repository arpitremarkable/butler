from brunch.models import DatabaseConfig, DatabaseColumnOption

from django import forms


class BaseModelForm(forms.ModelForm):
    class Meta:
        exclude = ('creator', 'editor', 'default_column_options', 'column_options', )


class DatabaseConfigModelForm(BaseModelForm):
    class Meta(BaseModelForm.Meta):
        model = DatabaseConfig


class DatabaseColumnOptionModelForm(BaseModelForm):
    class Meta(BaseModelForm.Meta):
        model = DatabaseColumnOption

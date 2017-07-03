from brunch.models import DatabaseSourceConfig, DatabaseTargetConfig, DatabaseColumnOption

from django import forms


class BaseModelForm(forms.ModelForm):
    class Meta:
        exclude = ('creator', 'editor', '_content_type', )


class DatabaseSourceConfigModelForm(BaseModelForm):
    class Meta(BaseModelForm.Meta):
        model = DatabaseSourceConfig


class DatabaseTargetConfigModelForm(BaseModelForm):
    class Meta(BaseModelForm.Meta):
        model = DatabaseTargetConfig


class DatabaseColumnOptionModelForm(BaseModelForm):
    class Meta(BaseModelForm.Meta):
        model = DatabaseColumnOption

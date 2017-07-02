from embulk.models import DatabaseConfig, DatabaseColumnOption

from django import forms


# class BaseConfigForm(forms.Form):
#     name = forms.CharField()

# class EmbulkConfig(object):
#     pass


# class DatabaseConfigForm(BaseConfigForm):
#     connection_name = forms.ChoiceField(choices=to_namedtuple(settings.DATABASES.keys()).__dict__.items())
#     select = forms.CharField(widget=widgets.Textarea(attrs={'rows': 2, 'cols': 100}))
#     table = forms.CharField()
#     where = forms.CharField(required=False, widget=widgets.Textarea(attrs={'rows': 2, 'cols': 100}))
#     batch_size = forms.IntegerField(required=False, initial=10000)
#     incremental_columns = SimpleArrayField(
#        base_field=forms.CharField(), widget=widgets.TextInput(attrs={'size': 40}), required=False
#     )
#     default_column_options = SplitArrayField(
#        base_field=forms.CharField(widget=widgets.TextInput(attrs={'size': 40}), required=False), size=3, required=False
#     )
#     column_options = default_column_options


# class DatabaseColumnOptionForm(BaseConfigForm):
#     value_types = to_namedtuple((
#         'long', 'double', 'float', 'decimal', 'boolean', 'string', 'json', 'date', 'time', 'timestamp',
#     ))
#     types = to_namedtuple(('boolean', 'long', 'double', 'string', 'json', 'timestamp', ))

#     name = forms.CharField(help_text='Column name used in select')
#     value_type = forms.ChoiceField(
#         label='Cast as', required=False, choices=value_types.__dict__.items()
#     )
#     type = forms.ChoiceField(label='Convert to', required=False, choices=types.__dict__.items())
#     timestamp_format = forms.CharField(
#         required=False, help_text='default : %Y-%m-%d for date, %H:%M:%S for time, %Y-%m-%d %H:%M:%S for timestamp'
#     )

class BaseModelForm(forms.ModelForm):
    class Meta:
        exclude = ('creator', 'editor', 'default_column_options', 'column_options', )


class DatabaseConfigModelForm(BaseModelForm):
    # connection_name = forms.ChoiceField(choices=to_namedtuple(settings.DATABASES.keys()).__dict__.items())
    # select = forms.CharField(widget=widgets.Textarea(attrs={'rows': 2, 'cols': 100}))
    # table = forms.CharField()
    # where = forms.CharField(required=False, widget=widgets.Textarea(attrs={'rows': 2, 'cols': 100}))
    # batch_size = forms.IntegerField(required=False, initial=10000)
    # incremental_columns = SimpleArrayField(
    #     base_field=forms.CharField(), widget=widgets.TextInput(attrs={'size': 40}), required=False
    # )
    # default_column_options = SplitArrayField(
    #     base_field=forms.CharField(widget=widgets.TextInput(attrs={'size': 40}), required=False), size=3, required=False
    # )
    # column_options = default_column_options

    class Meta(BaseModelForm.Meta):
        model = DatabaseConfig


class DatabaseColumnOptionModelForm(BaseModelForm):

    class Meta(BaseModelForm.Meta):
        model = DatabaseColumnOption

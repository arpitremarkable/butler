import os
import tempfile

from django.conf import settings


class EmbulkConfig(object):
    pass


class DatabaseConfig(object):

    def __init__(self, using, **options):
        from django.db import connections
        self.connection = connections[using]
        self.config = dict(filter(lambda d: bool(d[1]), {
            'type': self.connection.vendor,
            'host': self.connection.settings_dict['HOST'],
            'user': self.connection.settings_dict['USER'],
            'password': self.connection.settings_dict['PASSWORD'],
            'database': self.connection.settings_dict['NAME'],
            'port': self.connection.settings_dict['PORT'],
            'default_timezone': settings.TIME_ZONE,
        }.items()))
        self.config.update(options)


class InputConfig(EmbulkConfig):
    pass


class OutputConfig(EmbulkConfig):
    pass


class CSVFileInputConfig(InputConfig):

    @staticmethod
    def _get_columns(column_options):
        columns = []
        for column, options in column_options.items():
            columns.append({'name': column, 'type': options['type'], 'format': options['timestamp_format']})
        return columns

    def __init__(self, path, column_options, **options):
        self.config = dict(filter(lambda d: bool(d[1]), {
            'type': 'file',
            'path_prefix': path,
            'parser': {
                'charset': 'UTF-8',
                'newline': 'CRLF',
                'type': 'csv',
                'columns': self._get_columns(column_options),
                'stop_on_invalid_record': True,
                'skip_header_lines': 1,
                'default_timezone': settings.TIME_ZONE,
            }
        }.items()))
        self.config.update(options)


class DatabaseInputConfig(DatabaseConfig, InputConfig):
    pass


class DatabaseOutputConfig(DatabaseConfig, OutputConfig):
    def __init__(self, **options):
        super(DatabaseOutputConfig, self).__init__(**options)
        if self.config['type'] == 'redshift':
            from django.conf import settings
            self.config.update({
                'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
                'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
                'iam_user_name': settings.IAM_USER_NAME,
                's3_bucket': self.connection.settings_dict['S3_BUCKET'],
                's3_key_prefix': self.connection.settings_dict['S3_KEY_PREFIX'],
                'temp_schema': self.connection.settings_dict['LOADING_SCHEMA'],
            })


class CSVOutputConfig(OutputConfig):

    def __init__(self, file_path=tempfile.gettempdir(), **options):
        self.config = {
            'type': 'command',
            'command': "cat - > %s" % (os.path.join(file_path, 'task.$INDEX.$SEQID.csv'), ),
            'formatter': {
                'type': 'csv',
            },
        }
        self.config.update(options)

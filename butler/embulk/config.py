import os
import tempfile

import yaml


class EmbulkConfig(object):
    pass


class EmbulkDatabaseConfig(object):

    def __init__(self, using, **options):
        from django.conf import settings
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


class EmbulkInputConfig(EmbulkConfig):
    pass


class EmbulkOutputConfig(EmbulkConfig):
    pass


class EmbulkDatabaseInputConfig(EmbulkDatabaseConfig, EmbulkInputConfig):
    pass


class EmbulkDatabaseOutputConfig(EmbulkDatabaseConfig, EmbulkOutputConfig):
    pass


class EmbulkRedshiftOutputConfig(EmbulkDatabaseOutputConfig):

    def __init__(self, **options):
        from django.conf import settings
        super(EmbulkRedshiftOutputConfig, self).__init__(**options)
        self.config.update({
            'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            'iam_user_name': settings.IAM_USER_NAME,
            's3_bucket': self.connection.settings_dict['S3_BUCKET'],
            's3_key_prefix': self.connection.settings_dict['S3_KEY_PREFIX'],
            'temp_schema': self.connection.settings_dict['LOADING_SCHEMA'],
        })


class EmbulkCSVOutputConfig(EmbulkOutputConfig):

    def __init__(self, file_path=tempfile.gettempdir(), **options):
        self.config = {
            'type': 'command',
            'command': "cat - > %s" % (os.path.join(file_path, 'task.$INDEX.$SEQID.csv'), ),
            'formatter': {
                'type': 'csv',
            },
        }
        self.config.update(options)


def build_config(input, output):
    def get_yaml(dic):
        return yaml.dump(dic)

    config = {
        'in': input.config,
        'out': output.config,
    }
    print(yaml.dump(config))

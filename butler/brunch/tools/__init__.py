from django.conf import settings

from brunch.tools.embulk import CSVFileInputConfig, DatabaseInputConfig, DatabaseOutputConfig

import os
import yaml


def clean_dict(dic):
    return dict(filter(lambda d: bool(d[1]), dic.items()))


def get_column_options(config):
    options = {}
    for option in config.column_options.all():
        options[option.name] = clean_dict({
            'value_type': option.value_type,
            'type': option.type,
            'timestamp_format': option.timestamp_format,
        })
    return options


def execute(source_config, target_config, task):
    if source_config.NATURE == 'database':
        input = DatabaseInputConfig(
            using=source_config.connection_name,
            select=source_config.select,
            table=source_config.table,
            where=source_config.where,
            order_by=source_config.order_by,
            fetch_rows=source_config.batch_size,
            incremental=bool(source_config.incremental_columns),
            incremental_columns=source_config.incremental_columns,
            column_options=get_column_options(source_config),
        )
    elif source_config.NATURE == 'explorer':
        input = DatabaseInputConfig(
            using=source_config.connection_name,
            query=source_config.query.sql,
            column_options=get_column_options(source_config),
            fetch_rows=source_config.batch_size,
        )
    elif source_config.NATURE == 'file':
        # Only csv supported right now
        input = CSVFileInputConfig(
            path=source_config.file.path,
            column_options=get_column_options(source_config),
        )
    else:
        raise Exception('Not implemented %s input type' % (source_config.NATURE, ))

    if target_config.NATURE == 'database':
        output = DatabaseOutputConfig(
            using=target_config.connection_name,
            table=target_config.table,
            mode=target_config.mode,
            merge_keys=target_config.merge_keys,
            column_options=get_column_options(target_config),
        )
    else:
        raise Exception('Not implemented %s output type' % (target_config.NATURE, ))

    def build_config(input, output):
        config = {
            'in': clean_dict(input.config),
            'out': clean_dict(output.config),
        }
        return config

    seed_config_file = os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'seed_config_task_%d.yaml' % task.id)
    config_file = os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_task_%d.yaml' % task.id)
    resume_file = os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_task_%d_resume_state.yaml' % task.id)
    result_file = os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_task_%d.stdout' % task.id)
    config_diff_file = os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_diff_task_%d.yaml' % task.id)
    with open(seed_config_file, 'w+') as outfile:
        yaml.safe_dump(build_config(input, output), outfile, default_flow_style=False)
        from subprocess import Popen
        os.remove(config_file)
        process = Popen([' '.join([
            os.path.join(settings.EMBULK_PATH, 'embulk'),
            'guess',
            seed_config_file,
            '-o',
            config_file,
        ])], shell=True)
        process.wait()

    with open(result_file, 'w+') as result_file_fd:
        from subprocess import Popen
        process = Popen([' '.join([
            os.path.join(settings.EMBULK_PATH, 'embulk'),
            'run',
            config_file,
            '-r',
            resume_file,
            '-c' if input.PRESERVE_CONFIG_DIFF else '',
            config_diff_file if input.PRESERVE_CONFIG_DIFF else '',
            '-l',
            'debug',
        ])], stdout=result_file_fd, shell=True)
        ret_code = process.wait()
        result_file_fd.flush()
        return ret_code

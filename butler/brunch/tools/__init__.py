from django.conf import settings

from brunch.tools.embulk import DatabaseInputConfig, DatabaseOutputConfig

import os
import yaml


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
        )
    else:
        raise Exception('Not implemented %s input type' % (source_config.NATURE, ))

    if target_config.NATURE == 'database':
        output = DatabaseOutputConfig(
            using=target_config.connection_name,
            table=target_config.table,
            mode=target_config.mode,
            merge_keys=target_config.merge_keys,
        )
    else:
        raise Exception('Not implemented %s output type' % (target_config.NATURE, ))

    def build_config(input, output):
        def clean(dic):
            return dict(filter(lambda d: bool(d[1]), dic.items()))
        config = {
            'in': clean(input.config),
            'out': clean(output.config),
        }
        return config

    config_file = os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_task_%d.yaml' % task.id)
    resume_file = os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_task_%d_resume_state.yaml' % task.id)
    result_file = os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_task_%d.stdout' % task.id)
    config_diff_file = os.path.join(settings.EMBULK_PATH, '../brunch/configs/', 'config_diff_task_%d.yaml' % task.id)
    with open(config_file, 'w+') as outfile:
        yaml.safe_dump(build_config(input, output), outfile, default_flow_style=False)

    with open(result_file, 'w+') as result_file_fd:
        from subprocess import Popen
        process = Popen([' '.join([
            os.path.join(settings.EMBULK_PATH, 'embulk'),
            'run',
            config_file,
            '-r',
            resume_file,
            '-c',
            config_diff_file
        ])], stdout=result_file_fd, shell=True)
        ret_code = process.wait()
        result_file_fd.flush()
        return ret_code

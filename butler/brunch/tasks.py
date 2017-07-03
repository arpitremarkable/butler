from __future__ import absolute_import, unicode_literals

from celery import shared_task

from brunch import tools
from brunch.models import ScheduledTask


# def build_config(source_config, target_config):
#     def get_yaml(dic):
#         return yaml.dump(dic)

#     config = {
#         'in': input.config,
#         'out': output.config,
#     }
#     print(yaml.dump(config))


@shared_task
def execute_config(scheduled_task_id, *args, **kwargs):
    task = ScheduledTask.objects.get(id=scheduled_task_id)
    source_config = task.source_config.special_object
    target_config = task.target_config.special_object

    tools.execute(source_config, target_config, task)
    print(source_config, target_config)
    return source_config, target_config

    # config = build_config(source_config, target_config)
    # write_config(config, )

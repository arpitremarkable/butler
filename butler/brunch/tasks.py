from __future__ import absolute_import, unicode_literals

from celery import shared_task

from brunch import tools
from brunch.models import ScheduledTask


@shared_task
def execute_config(scheduled_task_id, *args, **kwargs):
    task = ScheduledTask.objects.get(id=scheduled_task_id)
    source_config = task.source_config.special_object
    target_config = task.target_config.special_object

    ret_code = tools.execute(source_config, target_config, task)
    if ret_code:
        raise Exception("Task %s failed with ret_code %s" % (scheduled_task_id, ret_code, ))

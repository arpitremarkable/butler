from __future__ import absolute_import, unicode_literals

from celery import shared_task

from brunch import tools
from brunch.models import ScheduledTask


@shared_task(bind=True)
def execute_config(self, scheduled_task_id, *args, **kwargs):
    task = ScheduledTask.objects.get(id=scheduled_task_id)
    source_config = task.source_config.special_object
    target_config = task.target_config.special_object
    try:
        ret_code = tools.execute(source_config, target_config, task)
    except Exception as e:
        raise self.retry(exc=e)
    try:
        assert not ret_code
    except AssertionError:
        raise self.retry(exc=Exception("Task %s failed with ret_code %s" % (scheduled_task_id, ret_code, )))

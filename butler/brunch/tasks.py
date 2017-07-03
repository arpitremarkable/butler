from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def execute_config(config_id, *args, **kwargs):
    from brunch.models import Config
    # from brunch.tools import Config
    config = None
    base_config = Config.objects.get(id=config_id)
    if hasattr(base_config, 'databaseconfig'):
        config = base_config.databaseconfig
    return config

    # if config
    #     build_config(database_config)

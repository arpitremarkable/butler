celery_worker: cd butler && celery -A butler worker -l debug
celery_beat: cd butler && celery beat -A butler -l debug -S django
django_server: cd butler && python manage.py runserver

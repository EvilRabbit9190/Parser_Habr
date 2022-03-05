import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parsingHabr.settings')

app = Celery('my_parse_habr')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Run a periodic task
app.conf.beat_schedule = {"Request-main-page": {
        'task': 'getHubs.tasks.request_to_main_hub',
        'schedule': crontab(minute='*/8'), # Run every 8 minutes
        'args': (),
}}

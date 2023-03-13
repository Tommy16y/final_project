import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault("DJANGO_SETTINGS_MODULE","main.settings")

app = Celery("main")

app.config_from_object("django.conf.settings",namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_spam':{
        'task': 'spam.tasks.send_spam',
        'schedule': crontab(minute='*/1')
    }
}
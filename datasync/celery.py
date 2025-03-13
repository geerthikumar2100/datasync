import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datasync.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

celery_app = Celery('datasync')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

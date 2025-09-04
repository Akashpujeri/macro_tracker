import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marco_tracker.settings')
app = Celery('marco_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

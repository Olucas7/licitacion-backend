from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('proc_eval_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
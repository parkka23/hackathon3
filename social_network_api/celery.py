import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network_api.settings')

app = Celery('social_network_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')

#
# app.conf.beat_schedule = {
#     'send-spam-every-5-minute': {
#         'task': 'social_network_api.tasks.send_beat_email',
#         'schedule': crontab(minute='*/5')
#     }
# }

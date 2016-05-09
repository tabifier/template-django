import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__app__.settings')

app = Celery('worker')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Needed to setup sentry logging from celery tasks
# See: https://github.com/getsentry/raven-python/issues/425#issuecomment-59098298
if hasattr(settings, 'SENTRY_DSN'):
    from raven.contrib.django.models import client
    from raven.contrib.celery import register_signal

    register_signal(client)

import logging

from __app__.celery_worker import app
from notifications.channels import Channels
from notifications.constants import notification_events, SLACK, DB, EMAIL

logger = logging.getLogger(__name__)


@app.task
def notify(event_name, *args, **kwargs):
    if event_name in notification_events.keys():
        event_details = notification_events[event_name]
        for channel in event_details.get('channels', []):
            if channel == DB:
                notify_db.delay(event_name, *args, **kwargs)
            elif channel == EMAIL:
                notify_email.delay(event_name, *args, **kwargs)
            elif channel == SLACK:
                notify_slack.delay(event_name, *args, **kwargs)


@app.task
def notify_db(event_name, *args, **kwargs):
    Channels.db.notify(event_name, *args, **kwargs)


@app.task
def notify_email(event_name, *args, **kwargs):
    Channels.email.notify(event_name, *args, **kwargs)


@app.task
def notify_slack(event_name, *args, **kwargs):
    Channels.slack.notify(event_name, *args, **kwargs)

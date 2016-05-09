import logging

from __app__.celery_worker import app
from django.conf import settings
from emails.utils import (
    send_email as sync_send_email,
    send_templated_email as sync_send_templated_email
)

logger = logging.getLogger(__name__)


@app.task
def send_email(to, subject, message_text, message_html=None, sender=settings.DEFAULT_FROM_EMAIL, async=True):
    sync_send_email(to, subject, message_text, message_html=None, sender=settings.DEFAULT_FROM_EMAIL, async=False)


@app.task
def send_templated_email(email_type, to, async=True, **kwargs):
    sync_send_templated_email(email_type, to, async=False, **kwargs)

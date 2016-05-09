import collections
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from emails.constants import EMAILS


def deep_update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = deep_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def send_email(to, subject, message_text, message_html=None, sender=settings.DEFAULT_FROM_EMAIL):
    email = EmailMultiAlternatives(subject, message_text)
    if message_html:
        email.attach_alternative(message_html, "text/html")
    email.to = [to]
    email.from_email = sender
    email.send()


def send_templated_email(email_type, to, **kwargs):
    if email_type in EMAILS and EMAILS[email_type].get('is_active', True):
        email = EMAILS[email_type]
        context = {}
        deep_update(context, email)
        deep_update(context, kwargs)

        message_html = ''
        message_text = ''
        if 'text_template' in email:
            message_text = render_to_string(email.get("text_template"), context)
        if 'html_template' in email:
            message_html = render_to_string(email.get("html_template"), context)

        send_email(to, subject=context.get('subject', ''), message_text=message_text, message_html=message_html, sender=context.get('sender', None))

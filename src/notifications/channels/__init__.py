from notifications.channels.db import DBChannel
from notifications.channels.email import EmailChannel
from notifications.channels.slack import SlackChannel

DB = 'DB'
EMAIL = 'Email'
SLACK = 'Slack'


class Channels(object):
    db = DBChannel
    email = EmailChannel
    slack = SlackChannel

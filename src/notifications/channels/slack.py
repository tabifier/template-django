import json
import logging
import requests
from django.conf import settings

from notifications.channels.base import ChannelBase
from notifications.channels.handlers.slack import default_message_generator
from notifications.channels.handlers.slack.auth import get_user_signup_message


logger = logging.getLogger(__name__)
slack_events = {
    'api.roller_auth.user.signup': {'generator': get_user_signup_message, 'channel': '#roller-new-signups'},
    'api.notifications.slack.ping': {'generator': default_message_generator, 'channel': '#random'},
}
    

class SlackChannel(ChannelBase):
    @staticmethod
    def notify(event_name, *args, **kwargs):
        should_ignore_notification = not all([
            getattr(settings, 'NOTIFICATIONS_SLACK_WEBHOOKS_URL', None),
            event_name in slack_events.keys(),
        ])
        if should_ignore_notification:
            return
        
        try:
            message = {
                'username': settings.NOTIFICATIONS_SLACK_USERNAME,
                'icon_url': settings.NOTIFICATIONS_SLACK_ICON_URL.replace('\'', ''),
                'channel': slack_events[event_name].get('channel', '#general'),
                'attachments': slack_events[event_name]['generator'](*args, **kwargs),
                'mrkdwn': True,
            }
            params = {'payload': json.dumps(message)}
            response = requests.post(settings.NOTIFICATIONS_SLACK_WEBHOOKS_URL, data=params)
            if response.status_code > 299:

                logger.error('notification - slack - error posting', extra={'details': {
                    'channel': message['channel'],
                    'status_code': response.status_code,
                    'body': response.content,
                }})
        except Exception, ex:
            logger.error(u'notification - slack - error posting', type(ex), exc_info=True)
            pass

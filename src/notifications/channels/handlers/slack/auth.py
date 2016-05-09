import logging

from django.contrib.auth.models import User

from geoip_data.utils import geoIP
    
logger = logging.getLogger(__name__)


def get_user_signup_message(user_id=None, ip_address=None, user_agent=None, referer=None, *args, **kwargs):
    if not user_id:
        return
        
    user = User.objects.get(id=user_id)
    user_count = User.objects.filter().count()
    
    slack_message = (
        'New user signup  :grinning: \n'
        '*email:* {email} \n'
        '*ip:* {ip_address} \n'
        '*user_agent:* {user_agent} \n'
        '*referer:* {referer}'
    ).format(email=user.email, ip_address=ip_address, user_agent=user_agent, referer=referer)

    geo = geoIP(ip_address)
    slack_attachments = [{
        'fallback': slack_message,
        'color': '#00BCD4',
        'pretext': 'New user signed up :grinning:',
        'title': user.email,
        'fields': [{
            'title': 'User count',
            'value': user_count,
            'short': True,
        }, {
            'title': 'IP Address',
            'value': ip_address,
            'short': True,
        }, {
            'title': 'Country',
            'value': geo['country_code'] or '',
            'short': True,
        }, {
            'title': 'City/State',
            'value': u'{}, {}'.format(geo['city'] or '', geo['region'] or '').lstrip(', ').rstrip(', '),
            'short': True,
        }, {
            'title': 'Referer',
            'value': referer,
            'short': False,
        }, {
            'title': 'User agent',
            'value': user_agent,
            'short': False,
        }]
        
    }]
    return slack_attachments

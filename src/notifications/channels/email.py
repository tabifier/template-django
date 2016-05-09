from django.conf import settings
from django.contrib.auth.models import User
from emails.constants import EmailTypes
from emails.tasks import send_templated_email

from notifications.channels.base import ChannelBase

email_events = {
    'api.roller_auth.user.signup': EmailTypes.AUTH_WELCOME_EMAIL,
    'api.roller_auth.email.signup_verification:request': EmailTypes.AUTH_VERIFY_SIGNUP_EMAIL,
}


class EmailChannel(ChannelBase):

    @staticmethod
    def notify(event_name, user_id=None, email__to=None, *args, **kwargs):
        # reject any falsey value
        if not user_id and not email__to:
            return

        if event_name not in email_events:
            return

        to = email__to
        user = User.objects.get(id=user_id)
        if not to:
            to = user.email

        if event_name == 'api.roller_auth.email.signup_verification:request':
            cta = {}

            verification_key = user.login_emails.filter(is_active=True, email=to).values_list('verification_key', flat=True)
            if len(verification_key) == 1:
                cta['button_link'] = settings.APP_EMAIL_CONFIRMATION_URL.format(verification_key[0])
                kwargs['cta'] = cta

        send_templated_email(email_events[event_name], to, **kwargs)

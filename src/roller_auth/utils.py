import datetime

from django.conf import settings
from django.utils.timezone import now as utcnow

from oauth2_provider.models import Application
from oauthlib.common import generate_token


def generate_app_token(user):
    application = Application.objects.get(
        id=settings.OAUTH_APP__SYSTEM_CLIENT__ID,
        user__id=settings.SYSTEM_USER_ID
    )

    now = utcnow()
    delta_in_seconds = settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']
    expiry_datetime = now + datetime.timedelta(seconds=delta_in_seconds)

    access_token = user.accesstoken_set.create(
        token=generate_token(),
        application=application,
        scope=' '.join(settings.OAUTH_APP__SYSTEM_CLIENT__SCOPE),
        expires=expiry_datetime,
    )
    return access_token

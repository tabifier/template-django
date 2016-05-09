import logging

from __app__.celery_worker import app
from roller_auth.models import UserProfile
from notifications.tasks import notify

logger = logging.getLogger(__name__)


@app.task
def generate_profile_pictures(user_id):
    profile = UserProfile.objects.get(user__id=user_id)
    print 'generating profile pictures for ' + profile.user.email


@app.task
def signup_followup(user_id, ip_address, user_agent, referer, cookies):
    # log the signup
    # send welcome email
    notify.delay('api.roller_auth.user.signup', user_id, ip_address, user_agent, referer, cookies)

@app.task
def verify_email(user_id, email):
    notify.delay('api.roller_auth.email.signup_verification:request', user_id, email__to=email)

import random
import datetime
from hashlib import sha1

from django.conf import settings
from django.db import models
from django.utils import timezone


class UserEmailManager(models.Manager):

    def make_random_key(self, email):
        salt = sha1(str(random.random())).hexdigest()[:5]
        key = sha1(u"{}{}".format(salt, email).encode("utf-8")).hexdigest()
        return key

    def create_unverified_email(self, email, user=None, send_verification=True):
        email_obj = self.create(
            email=email,
            user=user,
            verification_key=self.make_random_key(email)
        )

        if send_verification:
            email_obj.send_verification_email()

        return email_obj

    def verify_email(self, verification_key):
        try:
            user_email = self.get(verification_key=verification_key)
        except self.model.DoesNotExist:
            return False

        if not user_email.verification_key_expired():
            user_email.verification_key = self.model.VERIFIED
            user_email.save()

            return user_email
        return False

    def delete_expired_unverified_emails(self):
        date_threshold = (timezone.now() - datetime.timedelta(days=settings.MAX_EMAIL_VERIFICATION_DAYS))
        expired_emails = self.filter(created__lt=date_threshold).exclude(is_verified=True)

        for email in expired_emails.iterator():
            if not email.is_default:
                email.delete()

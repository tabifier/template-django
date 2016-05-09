from random import Random

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField

from core.exceptions import GeneralErrorException
from roller_auth.constants import AuthErrorMessages, INITIALS_AVATAR_COLORS
from roller_auth.managers import UserEmailManager


class UserEmail(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='login_emails')
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    verification_key = models.CharField(max_length=40)

    objects = UserEmailManager()

    def __unicode__(self):
        return u"{} ({})".format(self.email, "verified" if self.is_verified else "unverified")

    def save(self, *args, **kwargs):
        '''
        Check that the project code and names are unique for the company
        '''
        errors = []

        if UserEmail.objects.filter(is_active=True, email__iexact=self.email).exclude(id=self.id).exists():
            errors.append(AuthErrorMessages.EMAIL_IN_USE)

        if errors:
            raise GeneralErrorException(data=errors)
        return super(UserEmail, self).save(*args, **kwargs)

    @property
    def is_default(self):
        if self.email == self.user.email:
            return True
        return False

    def make_default(self):
        self.user.email = self.email
        self.user.save()

    def set_as_verified(self):
        self.is_verified = True
        self.save()

    def send_verification_email(self):
        pass


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, related_name='profile')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    profile_color = models.CharField(max_length=7, null=False, default='#000', blank=False)
    profile_picture = models.ImageField(upload_to='media/profile-pictures/raw/%Y/%m/%d/', blank=True, max_length=255)
    phone_number = PhoneNumberField(blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.email


class UserMixin(object):
    '''
    Mixin used to add extra functionality to the User model.
    '''
    def __repr__(self):
        return u'<User: {} - "{}">'.format(self.email, "active" if self.is_active else "inactive")

    def get_initials(self):

        full_name = self.get_full_name().split()
        if not full_name:
            return "?"

        if len(full_name) > 1:
            return u''.join([full_name[0][0], full_name[-1][0]]).upper()
        return full_name[0][0].upper()

bases = [UserMixin]
[bases.append(base) for base in list(User.__bases__)]
User.__bases__ = tuple(bases)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            r = Random()
            UserProfile.objects.create(
                user=instance,
                profile_color=INITIALS_AVATAR_COLORS[r.randrange(0, len(INITIALS_AVATAR_COLORS))]
            )
            UserEmail.objects.create_unverified_email(
                email=instance.email,
                user=instance,
                send_verification=True
            )
        except (IntegrityError, GeneralErrorException) as ex:
            instance.delete()
            raise ex
    if not instance.is_active:
        for email in instance.login_emails.all():
            email.is_active = False
            email.save()

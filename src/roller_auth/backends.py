from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class EmailBackend(ModelBackend):
    """
    Authenticates against verified user emails.

    """
    def authenticate(self, email=None, password=None, *args, **kwargs):

        try:
            validate_email(email)

            additional_filters = {}
            # if getattr(settings, 'ALLOW_UNVERIFIED_EMAIL_LOGIN', True):
            #     additional_filters['login_emails__is_verified'] = True

            try:
                user = User.objects.get(login_emails__email__iexact=email, **additional_filters)
                if user.check_password(password) and user.is_active:
                    return user
            except User.DoesNotExist:
                pass

        except ValidationError:
            pass

        return None

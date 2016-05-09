from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from roller_auth.constants import AuthErrorMessages


class EmailAuthenticationForm(forms.Form):
    email = forms.CharField(label=_("Email"), max_length=75, error_messages={'required': AuthErrorMessages.FORM_REQUIRED_EMAIL})
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, error_messages={'required': AuthErrorMessages.FORM_REQUIRED_PASSWORD})

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError(AuthErrorMessages.LOGIN_INVALID_CREDENTIALS)

        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)

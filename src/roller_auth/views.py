import os
from datetime import datetime, timedelta
from uuid import uuid4

from django.contrib.auth import login, logout, get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.models import AccessToken
from oauth2_provider.views import ScopedProtectedResourceView

from core.exceptions import (
    InvalidCredentialException,
    GeneralErrorException,
    SerializerValidationException,
    UnAuthorizedAccessException,
)
from geoip_data.utils import geoIP
from roller_auth.backends import EmailBackend
from roller_auth.constants import AuthErrorMessages, SUPPORTED_PROFILE_PICTURE_FORMATS
from roller_auth.forms import EmailAuthenticationForm
from roller_auth.tasks import generate_profile_pictures, signup_followup, verify_email

from roller_auth.serializers import (
    LoginSerializer,
    LoginResponseSerializer,
    LogoutResponseSerializer,
    ServerResponseSerializer,
    SignupSerializer,
    UserSerializer,
)
from roller_auth.utils import generate_app_token
try:
    import version
except:
    version = None


class LoginLogoutMixin(object):

    def login(self, request, response, user):
        login(request=self.request, user=user)
        token = generate_app_token(self.request.user)
        expires = datetime.strftime(
            datetime.utcnow() + timedelta(seconds=settings.API_COOKIE_AGE),
            '%a, %d-%b-%Y %H:%M:%S GMT'
        )
        response.set_cookie(
            settings.API_COOKIE_NAME,
            token.token,
            expires=expires,
            domain=settings.API_COOKIE_DOMAIN
        )
        return response

    def logout(self, request, response):
        logout(request)
        for cookie in request.COOKIES:
            response.delete_cookie(cookie, domain=settings.API_COOKIE_DOMAIN)
        return response


class LoginView(LoginLogoutMixin, FormView):
    form_class = EmailAuthenticationForm
    template_name = 'roller_auth/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous():
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(LoginView, self).form_valid(form)
        response = self.login(self.request, response, form.get_user())
        return response

    def form_invalid(self, form):
        self.invalid_form = form
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        return '/admin'


class LogoutView(LoginLogoutMixin, RedirectView):
    url = reverse_lazy('roller_auth__login')

    def get(self, request, *args, **kwargs):
        response = super(LogoutView, self).get(request, *args, **kwargs)
        response = self.logout(request, response)
        return response

class APILoginView(APIView):

    # @method_decorator(sensitive_post_parameters())
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise SerializerValidationException(data=serializer.errors)

        user = EmailBackend().authenticate(**serializer.data)
        if not user:
            raise InvalidCredentialException()

        access_token = generate_app_token(user)

        response = LoginResponseSerializer({
            'access_token': access_token.token,
            'token_type': 'Bearer',
            'expires': access_token.expires,
            'scope': access_token.scope
        })

        return Response(response.data, status=status.HTTP_200_OK)


class APISignupView(APIView):

    # @method_decorator(sensitive_post_parameters())
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            raise SerializerValidationException(data=serializer.errors)

        UserModel = get_user_model()

        user = UserModel.objects.create(
            email=serializer.data['email'].lower(),
            username=str(uuid4()),
        )
        user.set_password(serializer.data['password'])
        user.save()
        access_token = generate_app_token(user)

        signup_followup.delay(
            user_id=user.id,
            ip_address=request.META.get('HTTP_X_REAL_IP'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            referer=request.META.get('HTTP_REFERER'),
            cookies=request.COOKIES
        )

        verify_email.delay(user_id=user.id, email=user.email)

        response = LoginResponseSerializer({
            'access_token': access_token.token,
            'token_type': 'Bearer',
            'expires': access_token.expires,
            'scope': access_token.scope
        })

        return Response(response.data, status=status.HTTP_200_OK)


class APILogoutView(APIView):

    def get(self, request, *args, **kwargs):
        access_tokens = []
        if not request.user.is_anonymous():
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            auth_query = request.GET.get('access_token')
            if auth_header.lower().index('bearer') == 0:
                access_tokens.append(auth_header[6:].strip())
            if auth_query:
                access_tokens.append(auth_query.strip())
            try:
                tokens = AccessToken.objects.filter(token__in=access_tokens)
                for token in tokens:
                    token.revoke()
            except Exception:
                # TODO: Log error
                pass

        response = LogoutResponseSerializer([
            {'access_token': token, 'deactivated': True} for token in set(access_tokens)
        ], many=True)
        return Response(response.data, status=status.HTTP_200_OK)


class APIUsersMeView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        response = UserSerializer(request.user)
        return Response(response.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)

        if not serializer.is_valid():
            raise SerializerValidationException(data=serializer.errors)

        serializer.update(instance=request.user, validated_data=serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIUploadProfilePicture(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if len(request.stream.FILES) != 1:
            raise GeneralErrorException(data=AuthErrorMessages.INVALID_NUMBER_OF_PROFILE_PICTURES_UPLOADED)

        upload = request.stream.FILES.keys()[0]
        content = request.stream.FILES[upload]
        ext = upload.split('.')[-1].lower()
        if content.content_type.startswith('image/') and ext in SUPPORTED_PROFILE_PICTURE_FORMATS:
            ext = '.{}'.format(ext)
        else:
            raise GeneralErrorException(data=AuthErrorMessages.UNSUPPORTED_PROFILE_PICTURE_FORMAT)

        content.name = '{}{}'.format(str(uuid4()), ext)

        profile = request.user.profile
        profile.profile_picture_raw = content
        profile.save()

        generate_profile_pictures.delay(request.user.id)
        return Response({'profile_picture': profile.profile_picture_raw.url}, status=status.HTTP_200_OK)


class ServerView(ScopedProtectedResourceView, APIView):
    required_scopes = ['owner']

    def get(self, request, *args, **kwargs):
        if not request.user or not request.user.is_staff:
            raise UnAuthorizedAccessException()

        server_details = {
            'request_ip': '{} :: {} :: {}'.format(
                request.META.get('HTTP_X_FORWARDED_FOR'),
                request.META.get('REMOTE_ADDR'),
                request.META.get('HTTP_X_REAL_IP')
            ),
            'geoip': geoIP(request.META.get('HTTP_X_REAL_IP')),
            'host': os.getenv('HOSTNAME'),
            'uptime': os.popen('uptime').read().strip().replace('\n', ''),
        }

        if version is not None:
            server_details['commit'] = version.COMMIT
            server_details['branch'] = version.BRANCH

        response = ServerResponseSerializer(server_details)
        return Response(response.data, status=status.HTTP_200_OK)

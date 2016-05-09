import os
import sys
import dj_database_url
import rest_framework

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'ljhpeofjpMHPH*@lLKjLKmg*Ho298hoqwonm98oon@#2noiysd')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG', 1)))
ENVIRONMENT_DOMAIN = os.getenv('ENVIRONMENT_DOMAIN')
ALLOWED_HOSTS = ['.{}'.format(ENVIRONMENT_DOMAIN)]

LOGIN_URL = 'https://api.{}/login/'.format(ENVIRONMENT_DOMAIN)
# Application definition

INSTALLED_APPS = [
    'gunicorn',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'oauth2_provider',
    'django_premailer',
    'corsheaders',
    'roller_auth',
    'geoip_data',
    'geography',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'roller_auth.middleware.RollerAPIMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'roller_auth.backends.EmailBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

MEDIA_URL = 'https://api.{}/'.format(ENVIRONMENT_DOMAIN)

ROOT_URLCONF = '__app__.urls'

APPEND_SLASH = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.settings',
            ],
        },
    },
]
VISIBLE_SETTINGS_IN_TEMPLATES = (
    'MEDIA_URL',
)

WSGI_APPLICATION = '__app__.wsgi.application'
AUTH_PROFILE_MODULE = 'roller_auth.UserProfile'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    # Note that the dj_database_url doesn't always work well with symbols in the
    # password field. Use at your own risk. ie. mysql://test:ab#!cd@mysqld/test_db
    'default': dj_database_url.config(default=os.getenv('DB_CONNECTION')),
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/assets/'
STATIC_ROOT = '/assets/'

SYSTEM_USER_ID = 1
SESSION_COOKIE_NAME = 'session'
SESSION_COOKIE_DOMAIN = '.{}'.format(ENVIRONMENT_DOMAIN)
SESSION_COOKIE_AGE = 30*24*60*60  # 30 days
API_COOKIE_NAME = 'token'
API_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN
API_COOKIE_AGE = SESSION_COOKIE_AGE
CSRF_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN


################################################################################
#                            EMAIL Host
################################################################################
DEFAULT_FROM_EMAIL = '<no-reply@{}>'.format(ENVIRONMENT_DOMAIN)
if bool(int(os.getenv('EMAIL_TO_CONSOLE', 1))):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_USE_TLS = bool(int(os.getenv('EMAIL_USE_TLS')))
    EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


################################################################################
#                            File Storage
################################################################################
if (bool(int(os.getenv('GS_ENABLED', 0)))):
    INSTALLED_APPS.append('storages')
    DEFAULT_FILE_STORAGE = 'storages.backends.gs.GSBotoStorage'
    GS_ACCESS_KEY_ID = os.getenv('GS_ACCESS_KEY_ID')
    GS_SECRET_ACCESS_KEY = os.getenv('GS_SECRET_ACCESS_KEY')
    GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')
    GS_QUERYSTRING_EXPIRE = int(os.getenv('GS_QUERYSTRING_EXPIRE', 3600))
    GS_DEFAULT_ACL = None

################################################################################
#                               GeoIP
################################################################################
GEOIP_PATH = os.path.join(BASE_DIR, 'geoip_data', 'data')
GEOIP_CITY = 'GeoLite2-City.mmdb'
GEOIP_STORAGE_BUCKET_NAME = 'api-tabifier-com'
################################################################################
#                            Celery Queue
################################################################################
if (bool(int(os.getenv('CELERY_ENABLED', 0)))):
    INSTALLED_APPS.append('djcelery')

    import djcelery
    djcelery.setup_loader()
    BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_SEND_TASK_ERROR_EMAILS = False
    CELERY_DEFAULT_QUEUE = 'djangoapp'
    CELERY_DEFAULT_EXCHANGE = 'djangoapp'
    CELERY_HIGH_PRIORITY_QUEUE = 'djangoapp:high_priority'
    CELERY_REDIRECT_STDOUTS = False
    CELERY_NUM_NODES = 2
    CELERY_ALWAYS_EAGER = True  # bool(int(os.getenv('CELERY_ALWAYS_EAGER', 0)))
    CELERYD_HIJACK_ROOT_LOGGER = False
    CELERY_REDIRECT_STDOUTS_LEVEL = os.getenv('CELERY_REDIRECT_STDOUTS_LEVEL', 'WARNING')
    CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

################################################################################
#                            REST Framework
################################################################################
rest_framework.HTTP_HEADER_ENCODING = 'utf-8'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        # 'rest_framework.renderers.JSONRenderer',

    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        # 'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'EXCEPTION_HANDLER': 'core.exceptions.api_exception_handler',
}

MAX_EMAIL_VERIFICATION_DAYS = int(os.getenv('MAX_EMAIL_VERIFICATION_DAYS', 7))

DEFAULT_SCOPE = ('read', )
PRIVILEGED_SCOPE = ('owner', 'system')
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 90*24*60*60,
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups',
        'owner': 'Privileged access for the owner of an account.',
        'system': 'Privileged access to all system functionality.',
    }
}
OAUTH_APP__SYSTEM_CLIENT__ID = 1
OAUTH_APP__PERSONAL_ACCESS_TOKEN__ID = 2
OAUTH_APP__SYSTEM_CLIENT__SCOPE = ('owner', )
OAUTH_APP__PERSONAL_ACCESS_TOKEN__SCOPE = ('owner', )

# Enable CORS requests from any sub-domain on the env (*.ENVIRONMENT_DOMAIN)
CORS_ORIGIN_REGEX_WHITELIST = ('^https?://(\w+\.)?{}(:\d+)?$'.format(ENVIRONMENT_DOMAIN), )
if DEBUG:
    CORS_ORIGIN_REGEX_WHITELIST = ('^https?://((\w+\.)?{}|localhost)(:\d+)?$'.format(ENVIRONMENT_DOMAIN), )

################################################################################
#                         Notification Settings
################################################################################

NOTIFICATIONS_ENABLED = bool(int(os.getenv('NOTIFICATIONS_ENABLED', 0)))
if NOTIFICATIONS_ENABLED:
    NOTIFICATIONS_SLACK_USERNAME = os.getenv('NOTIFICATIONS_SLACK_USERNAME')
    NOTIFICATIONS_SLACK_ICON_URL = os.getenv('NOTIFICATIONS_SLACK_ICON_URL')
    NOTIFICATIONS_SLACK_WEBHOOKS_URL = os.getenv('NOTIFICATIONS_SLACK_WEBHOOKS_URL')

################################################################################
#                                 Logging
################################################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': sys.stdout,
        },
    },

    'loggers': {
        '': {
            'handlers': ['null', 'console', ],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}

################################################################################
#                            Sentry
################################################################################
if (bool(int(os.getenv('SENTRY_ENABLED', 0)))):
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }
    try:
        import version
        RAVEN_CONFIG['release'] = version.COMMIT
    except Exception:
        pass
        # On production, CircleCI creates version.py file which contains the
        # git release hash. If you want to grab the version from raven, use
        # the following 2 lines:
        # import raven
        # RAVEN_CONFIG['release'] = raven.fetch_git_sha(os.path.dirname(__file__))

    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.handlers.logging.SentryHandler',
        'dsn': SENTRY_DSN
    }

    LOGGING['loggers']['']['handlers'].append('sentry')


################################################################################
#                            Testing Settings
################################################################################
NOSE_ARGS = [
    '-aunit',
    '-aintegration',
    '--with-timer',
    '--timer-top-n=100',
    '--timer-ok=1',
    '--timer-warning=5',
]

# remove django `debug_toolbar` from installed apps
if ('debug_toolbar' in INSTALLED_APPS):
    INSTALLED_APPS = list(INSTALLED_APPS)
    INSTALLED_APPS.remove('debug_toolbar')

    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.remove('debug_toolbar.middleware.DebugToolbarMiddleware')

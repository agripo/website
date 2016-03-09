"""
Django settings for agripo_website project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%%w$#6a@7(@m2u6rup^lob1i49dhl82-iuuex207@t5a%zoypc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
NO_CACHE = True

# Some constants for dev, staging and production server
SERVER_TYPE_DEVELOPMENT = "DEVELOPMENT"
SERVER_TYPE_PRODUCTION = "PRODUCTION"
SERVER_TYPE_STAGING = "STAGING"
SERVER_TYPE = SERVER_TYPE_DEVELOPMENT
SERVER_URL = "not.a.real.server:1234"

TESTING_FUNCTIONALITIES = False

DOMAIN = "agripo-dev.brice.xyz"

# Defining the server url for the tests on the staging server
import sys
for arg in sys.argv:
    if 'liveserver' in arg and "staging." in arg:
        SERVER_URL = arg.split('=')[1]
        SERVER_TYPE = SERVER_TYPE_STAGING

    if 'testing' in arg:
        TESTING_FUNCTIONALITIES = True
        print("Functional Tests mode (without facebook)\n")
        DOMAIN = "localhost:8081"

ALLOWED_HOSTS = [DOMAIN, "127.0.0.1"]

# Application definition

INSTALLED_APPS = (
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'admin_helper',
    'functional_tests',
    'webdoc',
    # external apps
    'solo',
    'ckeditor',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.persona',
    'mathfilters',
)

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

BACKUP_KEY = '8sfqf4s5qsc13q54ergsd2'
BACKUP_PASSWORD = '5465qd21qs5cq'

# Using some apps only on !production servers
if SERVER_TYPE != SERVER_TYPE_PRODUCTION:
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    # Adding the auto-connect backend
    AUTHENTICATION_BACKENDS = (
        'core.authentication.NewUserAutoconnectionModelBackend',
    ) + AUTHENTICATION_BACKENDS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
try:
    from agripo_website.mail_settings import *
except ImportError:
    raise Exception("No mail_settings! Use agripo_website.mail_settings_model to create one")

# auth and allauth settings
LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/"

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = False
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = False

SOCIALACCOUNT_PROVIDERS = {
    'persona':
        {'AUDIENCE': DOMAIN}}

if not TESTING_FUNCTIONALITIES:
    INSTALLED_APPS += (
        'allauth.socialaccount.providers.facebook',
    )
    SOCIALACCOUNT_PROVIDERS['facebook'] = {
        'METHOD': 'js_sdk',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'gender', ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'}

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace']},
            {'name': 'styles', 'items': ['Format', 'Font', 'FontSize']},
            {'name': 'document', 'items': ['Source', '-', 'Print']},
            {'name': 'about', 'items': ['About']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
                                            '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
        ],
        'extraAllowedContent': 'iframe[*]',
    },
}

MEDIA_ROOT = '{}/media/'.format(BASE_DIR)
MEDIA_URL = '/media/'
FILE_UPLOAD_PERMISSIONS = 0o644

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'agripo_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['template', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'core.context_processors.cookies_notification',
                'core.context_processors.partners_box',
                'core.context_processors.last_news_box',
                'core.context_processors.bd_webdoc_slideshow',
                'core.context_processors.allauth_activation',
                'core.context_processors.backup_extra_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'agripo_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
if SERVER_TYPE != SERVER_TYPE_DEVELOPMENT:
    STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'core': {
            'handlers': ['console'],
        },
        'lists': {
            'handlers': ['console'],
        },
    },
    'root': {'level': 'INFO'},
}

# We can't disallow cache on production servers
if NO_CACHE and DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

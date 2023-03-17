"""
Django settings for TransferCreditGuide project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

# DONIGER: Added import os here going off of Prof. Sherriff's additions to settings.txt to fix common issues
from pathlib import Path
import dj_database_url
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lavbz$wk&8@o^!_%bxp5@7nnhk4#i01-t^b%*!$&dfee32b105'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# DONIGER: Added both the local host and herokuapp.com here to handled the DisallowedHost error as seen in Prof. Sherriff's additions.
ALLOWED_HOSTS = ['localhost','127.0.0.1','transfer-credit-guide.herokuapp.com']

SITE_ID = 3


SECURE_SSL_REDIRECT = True

# Application definition
INSTALLED_APPS = [
    'TransferGuide.apps.TransferguideConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "django_rq",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SOCIALACCOUNT_LOGIN_ON_GET=True

#background task setup



'''
RQ_QUEUES = {
    'default': {
         'HOST': 'localhost',
         'PORT': '6379',
         'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'),  # If you're
         'DB': 0,
         'DEFAULT_TIMEOUT': 480,
     }
    'with-sentinel': {
        'SENTINELS': [('localhost', 26736), ('localhost', 26737)],
        'MASTER_NAME': 'redismaster',
        'DB': 0,
        # Redis username/password
        'USERNAME': 'redis-user',
        'PASSWORD': 'secret',
        'SOCKET_TIMEOUT': 0.3,
        'CONNECTION_KWARGS': {  # Eventual additional Redis connection arguments
            'ssl': True
        },
        'SENTINEL_KWARGS': {    # Eventual Sentinel connection arguments
            # If Sentinel also has auth, username/password can be passed here
            'username': 'sentinel-user',
            'password': 'secret',
        },
    },
    
    'high': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'),#'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'), # If you're on Heroku
        'DEFAULT_TIMEOUT': 500,
    },
    
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}'''

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend'
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'TransferCreditGuide.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'TransferGuide/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TransferCreditGuide.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(default=os.environ['DATABASE_URL'])
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# DONIGER: Added the static_root variable here to fix an erorr with static files not being found as seen in Prof. Sherriff's additions
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# DONIGER copying Prof Sherriff's additions
# Activate Django-Heroku.
# Use this code to avoid the psycopg2 / django-heroku error!
# Do NOT import django-heroku above!
try:
    if 'HEROKU' in os.environ:
        import django_heroku
        django_heroku.settings(locals())
except ImportError:
    found = False

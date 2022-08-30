"""
Django settings for gogopowerkimibot project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from multiprocessing import set_start_method
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ytrf@-9)%tf^75!vxnm-zcv#^qeg8+68@yd!j8vp9tv1c&u_pc'

# Line Bot
LINE_CHANNEL_ACCESS_TOKEN = config(
    'LINE_CHANNEL_ACCESS_TOKEN', default='你的CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = config(
    'LINE_CHANNEL_SECRET', default='你的CHANNEL_SECRET')

# LINE Notify token
ZHIZHI_NOTIFY_TOKEN = config(
    'ZHIZHI_NOTIFY_TOKEN', default='你的LINI_NOTIFY_TOKEN')
CARBE_NOTIFY_TOKEN = config(
    'CARBE_NOTIFY_TOKEN', default='你的LINI_NOTIFY_TOKEN')
ETEN_NOTIFY_TOKEN = config(
    'ETEN_NOTIFY_TOKEN', default='你的LINI_NOTIFY_TOKEN')
CHOCO_NOTIFY_TOKEN = config(
    'CHOCO_NOTIFY_TOKEN', default='')
NETFLIXGRUP_NOTIFY_TOKEN = config(
    'NETFLIXGRUP_NOTIFY_TOKEN', default='')
YELMI_NOTIFY_TOKEN = config(
    'YELMI_NOTIFY_TOKEN', default='')

# CWB
CWB_TOKEN = config('CWB_TOKEN', default='')

# EPA
EPA_TOKEN = config('EPA_TOKEN', default='')

# Books Cookies
BOOKS_COOKIES = config('EPA_TOKEN', default='')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

# Mail
GMAIL_SMTP = config('GMAIL_SMTP', default='')
GMAIL_USER = config('GMAIL_USER', default='')
GMAIL_PASSWORD = config('GMAIL_PASSWORD', default='')
GMAIL_TLS_PORT = config('GMAIL_TLS_PORT', default='')

# CORS Config
# https://github.com/adamchainz/django-cors-headers
CORS_ORIGIN_WHITELIST = config(
    'WHITELIST', default='你的Domain').split(",")

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False

HOSTS_LIST = config(
    'HOSTS_LIST', default='你的Domain').split(",")
ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']
ALLOWED_HOSTS.extend(HOSTS_LIST)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gogopowerkimibot',
    'myconst',
    'utility',
    'django_q',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'gogopowerkimibot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'gogopowerkimibot.wsgi.application'

# CACHES
# https://docs.djangoproject.com/en/dev/topics/cache/
# CACHES Base on File
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    },
    "heroku": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_TLS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "ssl_cert_reqs": None,
                "max_connections": 18
            },
        }
    },
    "fly": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                # "ssl_cert_reqs": None,
                "max_connections": 18
            },
        }
    },
    'local': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# CACHES Base on Memory
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake',
#     }
# }

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRE_DATABASE', ""),
        'USER': config('POSTGRE_USER', ""),
        'PASSWORD': config('POSTGRE_PASSWORD', ""),
        'HOST': config('POSTGRE_HOST', ""),
        'PORT': config('POSTGRE_PORT', 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Q
Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 1,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}
# patch for Python 3.8
# https://github.com/Koed00/django-q/issues/389
set_start_method('fork')

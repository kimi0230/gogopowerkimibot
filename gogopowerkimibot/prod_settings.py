from .settings import *
STATIC_ROOT = 'staticfiles'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWD_HOSTS = ['*']
DEBUG = True

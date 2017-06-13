from .base import *

env = os.environ.get

DEBUG = env('DEBUG', 'off') == 'on'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app',
        'USER': env('POSTGRES_USER', 'root'),
        'PASSWORD': env('POSTGRES_PASSWORD', 'local'),
        'HOST': 'db',
        'PORT': '5432',

        'CONN_MAX_AGE': None,
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    },
}

ALLOWED_HOSTS = ['*', ]
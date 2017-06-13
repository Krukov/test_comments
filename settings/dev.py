from .docker import *

INSTALLED_APPS.extend([
    'django.contrib.sessions',  # for django toolbar
    'django.contrib.staticfiles',  # for django toolbar
    'debug_toolbar',
])

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
            ],
        },
    },
]
STATIC_URL = '/static/'

MIDDLEWARE.extend([
    'debug_toolbar.middleware.DebugToolbarMiddleware',
])

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda *args, **kwargs: True,
    'SHOW_COLLAPSED': True,
}

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')
REST_FRAMEWORK['DEFAULT_PARSER_CLASSES'].append('rest_framework.parsers.FormParser')
REST_FRAMEWORK['DEFAULT_PARSER_CLASSES'].append('rest_framework.parsers.MultiPartParser')

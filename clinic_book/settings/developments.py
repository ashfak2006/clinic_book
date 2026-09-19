
from .base import *




SECRET_KEY = 'django-insecure-tx656m)-1ko52gulnz5c4op7g#2yg#mzxscu433*l2foh8kh8n'

DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

from datetime import timedelta

SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'advistaadvertising@gmail.com'  # Your API Key username
EMAIL_HOST_PASSWORD = 'kmhq pmex mmss ypwv'

SPECTACULAR_SETTINGS = {
    "TITLE": "Clinic Book API",
    "DESCRIPTION": "Comprehensive API documentation for Clinic Book appointment and clinic management system.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}
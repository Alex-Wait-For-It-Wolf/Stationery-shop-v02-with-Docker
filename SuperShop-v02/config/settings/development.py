# development.py
from. _base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ['u!k*!%mk$zdb0vh-bw39u%1y+jvu-avc#wc11@jhi6el^uls^t']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 3

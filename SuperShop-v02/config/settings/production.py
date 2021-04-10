# production.py
from ._base import *

DEBUG = False

ADMINS = (
    ('Johnny_Mnemonic', 'emailtest@gmail.com'),
)

ALLOWED_HOST = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PSQL_DATABASE'),
        'USER': os.getenv('PSQL_USER'),
        'PASSWORD': os.getenv('PSQL_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '6432',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 3

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

params = {
    "username": EMAIL_HOST_USER,
    "password": EMAIL_HOST_PASSWORD,
    "to": ADMIN_EMAIL
}

handler = NotificationHandler("gmail", defaults=params)

logger.add(
    sink=handler,
    level="WARNING",
    enqueue=True,
    backtrace=True,
    diagnose=False
)

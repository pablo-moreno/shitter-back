from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

DEV_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]

MIDDLEWARE = DEV_MIDDLEWARE + MIDDLEWARE

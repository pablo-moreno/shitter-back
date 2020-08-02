import os


VERSION = os.environ.get('APP_VERSION')
SECRET_KEY = os.environ.get('SECRET_KEY', 'this-is-the-default-secret-key')
DEBUG = os.environ.get('DEBUG', True) is True

POSTGRES_DB = os.environ.get('POSTGRES_DB', 'postgres')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'postgres')
DATABASE_PORT = os.environ.get('DATABASE_PORT', 5432)
DATABASE_URL = os.environ.get('DATABASE_URL', f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{POSTGRES_DB}')

STATIC_ROOT = os.environ.get('STATIC_ROOT', 'static')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', 'media')

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

from .base import *
import os
import dj_database_url

DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get('SECRET_KEY')
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'images.apps.ImagesConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'easy_thumbnails',

]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'api-images',
        'USER': 'postgres',
        'PASSWORD': 'Pass',
        'HOST': 'localhost',
        'PORT': '',
    }
}
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

MEDIA_URL = '/api/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'api')
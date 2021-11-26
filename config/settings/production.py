from .base import *
import dj_database_url
import mimetypes
import os
import dj_database_url

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ["api-images-project.herokuapp.com", "localhost", "127.0.0.1"]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
mimetypes.add_type("text/css", ".css", True)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'images.apps.ImagesConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'easy_thumbnails',

]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['YOUR_CLOUD_NAME'],
    'API_KEY': os.environ['YOUR_API_KEY'],
    'API_SECRET': os.environ['YOUR_API_SECRET'],
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

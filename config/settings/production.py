from .base import *
import dj_database_url
import mimetypes

DEBUG = False

ALLOWED_HOSTS = ALLOWED_HOSTS = ["api-images-project.herokuapp.com", "localhost", "127.0.0.1"]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
mimetypes.add_type("text/css", ".css", True)

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)
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
    'whitenoise.runserver_nostatic',
    'cloudinary_storage',
    'cloudinary',

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['YOUR_CLOUD_NAME'],
    'API_KEY': os.environ['YOUR_API_KEY'],
    'API_SECRET': os.environ['YOUR_API_SECRET'],
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

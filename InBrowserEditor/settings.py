"""
Django settings for InBrowserEditor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lu6v=aj6z-s(f2gj6$+hv(1u^c*c7raswtnd%yi6wf$f0l5(@f'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
TEMPLATE_DEBUG = True
if os.getenv('ENV') == 'PROD':
    DEBUG = False
    TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','localhost','code-editor.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'editor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', #TEMP UNTIL FIX IS FOUND
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'InBrowserEditor.urls'

WSGI_APPLICATION = 'InBrowserEditor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {}
if os.getenv('ENV') == 'PROD':
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
if os.getenv('ENV') == 'PROD':
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
    

else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.file'

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
#To find the stored template views  
TEMPLATE_DIRS = (STATIC_URL,"editor"+STATIC_URL)

STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'editor/static'),)
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

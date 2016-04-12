## Copyright 2016 Raik Gruenberg

## This file is part of the LabHamster project (https://github.com/graik/labhamster). 
## LabHamster is released under the MIT open source license, which you can find
## along with this project (LICENSE) or at <https://opensource.org/licenses/MIT>.

"""
Django settings for labhamster project.
"""

# Build paths inside the project like this: os.path.join(PROJECT_ROOT, ...)
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# custom: distinguish development from production server
import sys
RUNNING_DEV_SERVER = ('runserver' in sys.argv)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''
try:
	## prepare env variable:
	## heroku config:add DJANGO_SECRET_KEY="your_secret_key"
	## Note: () are not tolerated in the key even using quotation marks
	SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or SECRET_KEY
except:
	pass
	
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Database configuration by Heroku $DATABASE_URL
# Use persistent connections
# https://devcenter.heroku.com/articles/django-app-configuration#database-connection-persistence
## this will be overriden by $DATABASE_URL configuration; sqlite is fall-back
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }}

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# https://devcenter.heroku.com/articles/django-app-configuration#static-assets-and-file-serving

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'labhamstersite','staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
##STATICFILES_DIRS = (
##    os.path.join(PROJECT_ROOT, 'static'),
##)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#
# Application definition
#
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'labhamster',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'labhamstersite.urls'

WSGI_APPLICATION = 'labhamstersite.wsgi.application'

# new in Django 1.9 default settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                 os.path.join(PROJECT_ROOT, 'labhamster', 'templates'),
                 os.path.join(PROJECT_ROOT, 'site_templates'),
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages"
            ],
        },
    },
]

# Activate SSL / HTTPS
if not RUNNING_DEV_SERVER:
	SECURE_SSL_REDIRECT = True # [1]
	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_L10N = False  ## de-activate automatic localization of numbers and dates
USE_TZ = True

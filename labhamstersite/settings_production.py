## Copyright 2016 Raik Gruenberg

## This file is part of the LabHamster project (https://github.com/graik/labhamster). 
## LabHamster is released under the MIT open source license, which you can find
## along with this project (LICENSE) or at <https://opensource.org/licenses/MIT>.


'''
Alternative settings file geared towards a postgresql + apache installation.
Modify and use instead of the default settings.py.

NOTE: This is based on a django 1.3.1 settings.py;
'''

DEBUG = True
TEMPLATE_DEBUG = True
ADMINS = ()
MANAGERS = ADMINS

DATABASES = {'default': 
             {'ENGINE': 'django.db.backends.postgresql_psycopg2',
             'NAME': 'labhamster',
             'USER': 'django',
             'PASSWORD': 'ENTER PASSWORD HERE',
             'HOST': '',
             'PORT': ''}}

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = False

DATE_FORMAT = 'y-m-d'

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder')

## change!!
SECRET_KEY = 'ENTER RANDOM KEY HERE'

TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader',
                    'django.template.loaders.filesystem.Loader')

MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')

ROOT_URLCONF = 'labhamsterproject.urls'
TEMPLATE_DIRS = ()

INSTALLED_APPS = ('django.contrib.admin',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'labhamster',
                  'south')

LOGGING = {'version': 1,
           'disable_existing_loggers': False,
           'handlers': {'mail_admins': {'level': 'ERROR',
                                        'class': 'django.utils.log.AdminEmailHandler'}},
           'loggers': {'django.request': {'handlers': ['mail_admins'],
                                          'level': 'ERROR',
                                          'propagate': True}}}

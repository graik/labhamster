"""
WSGI config for labhamstersite project. Adapted according to Heroku
python-getting-started app.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
https://devcenter.heroku.com/articles/django-app-configuration
"""
from __future__ import unicode_literals

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labhamstersite.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

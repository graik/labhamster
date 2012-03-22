import os
import sys

sys.path += ['/home/django/py']

os.environ['DJANGO_SETTINGS_MODULE'] = 'labhamsterproject.settings_local'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


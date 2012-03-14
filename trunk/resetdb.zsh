#!/usr/bin/zsh

python manage.py dumpdata --exclude auth --exclude contenttypes > datadump.json

python manage.py reset getitfast

python manage.py syncdb

python manage.py loaddata datadump.json

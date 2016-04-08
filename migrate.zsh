#!/usr/bin/zsh

export DJANGO_SITENAME=labhamsterdjango
export DJANGO_SETTINGS_MODULE=labhamsterdjango.settings

python manage.py schemamigration labhamster --auto

python manage.py migrate labhamster

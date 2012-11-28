#!/usr/bin/zsh

export DJANGO_SITENAME=labhamsterproject
export DJANGO_SETTINGS_MODULE=labhamsterproject.settings

python manage.py schemamigration labhamster --auto

python manage.py migrate labhamster

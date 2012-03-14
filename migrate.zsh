#!/usr/bin/zsh

python manage.py schemamigration labhamster --auto

python manage.py migrate labhamster

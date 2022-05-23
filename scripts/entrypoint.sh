#!/bin/sh

#Exit, if something go wrong
set -e

python manage.py collectstatic --noinput

uwsgi --socket :8000 --master --enable-threads --module face_recognition_project.wsgi
#!/bin/sh

python manage.py wait_for_db
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear
gunicorn fampay.wsgi -b 0.0.0.0:8000
#python manage.py runserver 0:8000

exec "$@"

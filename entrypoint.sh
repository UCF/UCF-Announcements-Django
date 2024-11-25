#!/bin/sh

cd /app
python manage.py migrate

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

exec gunicorn --workers=2 --threads=4 --worker-class=gthread --bind '[::]:80' --worker-tmp-dir /dev/shm wsgi:application

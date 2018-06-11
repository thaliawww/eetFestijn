#!/bin/bash

set -e

chown -R www-data:www-data /eetfestijn/
chown -R www-data:www-data /usr/src/app

cd /usr/src/app/

python /usr/src/app/manage.py migrate --no-input
python /usr/src/app/manage.py collectstatic --no-input

>&2 echo "Running site with uwsgi"
uwsgi --chdir /usr/src/app \
    --socket :8000 \
    --socket-timeout 1800 \
    --uid 33 \
    --gid 33 \
    --threads 5 \
    --processes 5 \
    --module eetfestijn.wsgi:application \
    --harakiri 1800 \
    --master \
    --max-requests 5000 \
    --vacuum \
    --limit-post 0 \
    --post-buffering 16384 \
    --thunder-lock \
    --logto '/eetfestijn/log/uwsgi.log'
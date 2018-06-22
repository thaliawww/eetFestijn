#!/bin/bash

set -e

cd /usr/src/app/
>&2 echo "Running ./manage.py $@"
./manage.py $@

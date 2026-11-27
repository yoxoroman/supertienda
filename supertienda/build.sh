#!/usr/bin/env bash
set -o errexit
pip install -r /supertienda/requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

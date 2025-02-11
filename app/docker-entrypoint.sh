#!/bin/sh
flask db init --directory data/
flask db migrate --directory data/
flask db upgrade --directory data/

gunicorn --worker-class eventlet -w 1 -b :8000 app:app --access-logfile ./logs/log.txt --log-level debug 
#!/bin/sh

find /app/www -name "*.pyc" -exec rm -rf {} \;

uwsgi --plugins-dir /usr/lib/uwsgi --ini /app/uwsgi.ini

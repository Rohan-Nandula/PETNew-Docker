#!/bin/sh

find /app/pet -name "*.pyc" -exec rm -rf {} \;

uwsgi --plugins-dir /usr/lib/uwsgi --ini /app/uwsgi.ini

#!/bin/sh
gunicorn management.wsgi --bind 0.0.0.0:5000 --chdir=/app


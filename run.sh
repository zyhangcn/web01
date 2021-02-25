#!/bin/sh
gunicorn config.wsgi --bind 0.0.0.0:5000 --chdir=/app


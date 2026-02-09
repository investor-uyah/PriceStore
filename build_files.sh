#!/bin/bash

# Allows installing packages without virtualenv, which is required for the build process
python3 -m pip install -r requirements.txt --break-system-packages

# Collect static files for production
python3 manage.py collectstatic --noinput
#!/bin/bash

# Exit on error
set -e

# Collect static files
python manage.py collectstatic --noinput

echo "Static files collected successfully."

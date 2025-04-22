#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements-render.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

# Create superuser (optional)
# python manage.py createsuperuser --noinput

# Print directory structure for debugging
echo "Directory structure:"
find . -type f -name "*.py" | sort

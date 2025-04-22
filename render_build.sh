#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Applying migrations..."
python manage.py migrate

echo "Directory structure:"
find . -type f -name "*.py" | grep -v "__pycache__" | sort

echo "WSGI file content:"
cat expense_splitter/wsgi.py

echo "Build completed successfully!"

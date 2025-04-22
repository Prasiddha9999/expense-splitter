#!/bin/bash
# This script is specifically for building the application on Render

set -o errexit  # Exit on error

# Print debugging information
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Files in current directory:"
ls -la

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Print more debugging information
echo "WSGI file content:"
cat expense_splitter/wsgi.py

echo "app.py content:"
cat app.py

echo "Directory structure:"
find . -type f -name "*.py" | grep -v "__pycache__" | sort

echo "Build completed successfully!"

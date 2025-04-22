#!/bin/bash
# This script is specifically for starting the application on Render
set -e  # Exit immediately if a command exits with a non-zero status

# Print debugging information
echo "=== RENDER STARTUP SCRIPT ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -m django --version)"
echo "Files in current directory:"
ls -la

# Set environment variables
export DJANGO_SETTINGS_MODULE=expense_splitter.production
export RENDER=true
export PRODUCTION=true

# Generate a secret key if not provided
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY="django-insecure-5h$at==31nq$3)^*^qon7nkbo&80v)e1lj2(s2t7tm1l&dtpa7"
    echo "WARNING: Using insecure default SECRET_KEY. Set SECRET_KEY environment variable in production."
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "WARNING: No DATABASE_URL environment variable set, will use SQLite instead."
fi

# Check if wsgi.py exists
if [ -f "expense_splitter/wsgi.py" ]; then
    echo "Found expense_splitter/wsgi.py"
    cat expense_splitter/wsgi.py
else
    echo "ERROR: expense_splitter/wsgi.py not found!"
fi

# Check if app.py exists
if [ -f "app.py" ]; then
    echo "Found app.py"
else
    echo "ERROR: app.py not found!"
fi

# Start Gunicorn with the correct application
echo "Starting Gunicorn with app:application"
exec gunicorn app:application

#!/bin/bash
# This script is specifically for starting the application on Render

# Print debugging information
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Files in current directory:"
ls -la

# Set environment variables
export DJANGO_SETTINGS_MODULE=expense_splitter.production
export RENDER=true
export PRODUCTION=true

# Start Gunicorn with the correct application
echo "Starting Gunicorn with expense_splitter.wsgi:application"
exec gunicorn expense_splitter.wsgi:application

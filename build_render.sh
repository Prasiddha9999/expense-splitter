#!/bin/bash
# This script is specifically for building the application on Render

set -o errexit  # Exit on error

# Print debugging information
echo "=== RENDER BUILD SCRIPT ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Files in current directory:"
ls -la

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p static media staticfiles

# Set environment variables for build process
export DJANGO_SETTINGS_MODULE=expense_splitter.production
export RENDER=true
export PRODUCTION=true
export SECRET_KEY="django-insecure-5h$at==31nq$3)^*^qon7nkbo&80v)e1lj2(s2t7tm1l&dtpa7"

# Check Django installation
echo "Checking Django installation..."
python -m django --version

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

# Create a test file to verify file system access
echo "Creating test file..."
echo "This is a test file created during the build process" > test_build_file.txt

# Check if SQLite database was created
if [ -f "db.sqlite3" ]; then
    echo "SQLite database created successfully"
else
    echo "WARNING: SQLite database not created"
fi

echo "Build completed successfully!"

"""
Direct WSGI entry point for Render deployment
"""

import os
import sys
import traceback

# Print debugging information
print("Starting app.py WSGI entry point")
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"Initial Python path: {sys.path}")

try:
    # Add the project directory to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    print(f"Updated Python path: {sys.path}")

    # Set environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_splitter.production')
    os.environ.setdefault('RENDER', 'true')
    os.environ.setdefault('PRODUCTION', 'true')

    # Generate a secret key if not provided
    if 'SECRET_KEY' not in os.environ:
        os.environ['SECRET_KEY'] = 'django-insecure-5h$at==31nq$3)^*^qon7nkbo&80v)e1lj2(s2t7tm1l&dtpa7'
        print('WARNING: Using insecure default SECRET_KEY. Set SECRET_KEY environment variable in production.')

    print(f"Environment variables set: DJANGO_SETTINGS_MODULE={os.environ.get('DJANGO_SETTINGS_MODULE')}")

    # List files in current directory
    print("Files in current directory:")
    for f in os.listdir(current_dir):
        print(f"  {f}")

    # Import the Django WSGI application
    print("Importing Django WSGI application...")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("Django WSGI application loaded successfully")

except Exception as e:
    print(f"ERROR: Failed to load WSGI application: {e}")
    traceback.print_exc()
    # Provide a minimal WSGI application for debugging
    def application(environ, start_response):
        status = '500 Internal Server Error'
        output = f'Error loading application: {str(e)}'.encode()
        response_headers = [('Content-type', 'text/plain'),
                           ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]

# Print final confirmation
print("WSGI entry point initialization complete")

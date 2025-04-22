"""
Direct WSGI entry point for Render deployment
"""

import os
import sys

# Add the project directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_splitter.production')
os.environ.setdefault('RENDER', 'true')
os.environ.setdefault('PRODUCTION', 'true')

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Print debugging information
if __name__ == '__main__':
    print("WSGI application loaded successfully")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

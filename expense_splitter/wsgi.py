"""
WSGI config for expense_splitter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Add the project directory to the Python path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

# Check for production environment
if os.environ.get('RENDER') or os.environ.get('PRODUCTION'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_splitter.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_splitter.settings')

# This application object is used by any WSGI server configured to use this file
application = get_wsgi_application()

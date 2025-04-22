"""
WSGI config for expense_splitter project.

This file contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_splitter.production')

# This application object is used by any WSGI server configured to use this file
application = get_wsgi_application()

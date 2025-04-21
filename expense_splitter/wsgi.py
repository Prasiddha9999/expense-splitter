"""
WSGI config for expense_splitter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Check for production environment
if os.environ.get('RENDER'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_splitter.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_splitter.settings')

application = get_wsgi_application()

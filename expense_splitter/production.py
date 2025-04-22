import os
import dj_database_url
from .settings import *

# Security settings
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# SECRET_KEY handling
SECRET_KEY = os.environ.get('SECRET_KEY')
# If SECRET_KEY is not set in environment, use a default one for development
if not SECRET_KEY:
    SECRET_KEY = 'django-insecure-5h$at==31nq$3)^*^qon7nkbo&80v)e1lj2(s2t7tm1l&dtpa7'
    print('WARNING: Using insecure default SECRET_KEY. Set SECRET_KEY environment variable in production.')

ALLOWED_HOSTS = ['expense-splitter.onrender.com', '.onrender.com', 'localhost', '127.0.0.1', '*']

# Database
# Use DATABASE_URL environment variable for database configuration
db_url = os.environ.get('DATABASE_URL')
if db_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    print(f'Using database configuration from DATABASE_URL')
else:
    # Fall back to SQLite if no DATABASE_URL is provided
    print('WARNING: No DATABASE_URL environment variable set, using SQLite instead')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add WhiteNoise middleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Media files
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# HTTPS settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

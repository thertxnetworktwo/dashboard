from .base import *

DEBUG = True

# Additional development settings
INSTALLED_APPS += [
    'django_extensions',
]

# Enable Django Debug Toolbar if needed
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INTERNAL_IPS = ['127.0.0.1']

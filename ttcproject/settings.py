"""
Django settings for ttcproject project.

This settings file determines which settings to use based on the environment.
It will detect if running on Vercel and use appropriate settings.
"""

import os

# Check if running on Vercel
IS_VERCEL = os.environ.get('VERCEL', '') == '1'

# Choose the right settings based on environment
if IS_VERCEL:
    from .settings_vercel import *
else:
    DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')
    if DJANGO_ENV == 'production':
        from .settings_prod import *
    else:
        from .settings_dev import *

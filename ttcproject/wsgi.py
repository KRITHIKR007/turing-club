"""
WSGI config for ttcproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Attempt to load .env file if exists (for production environments)
try:
    from dotenv import load_dotenv
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ttcproject.settings')

# This is needed for Vercel deployment
application = get_wsgi_application()

# For Vercel serverless function
app = application

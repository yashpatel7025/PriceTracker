"""
WSGI config for django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os



print('@'*50)
print(os.getcwd())
from pricetracker.pricetracker import settings
print('@'*50)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricetracker.pricetracker.settings')

application = get_wsgi_application()
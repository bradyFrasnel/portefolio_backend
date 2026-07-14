"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Utiliser settings_render.py si en production sur Render
if os.environ.get('RENDER') or not os.environ.get('DEBUG', 'True').lower() == 'true':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_render')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

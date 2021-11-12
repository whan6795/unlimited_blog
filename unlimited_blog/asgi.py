"""
ASGI config for unlimited_blog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

setting_file = os.environ.get('ENV', 'test')
print('wsgi settings:', setting_file)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.%s' % setting_file)

application = get_asgi_application()

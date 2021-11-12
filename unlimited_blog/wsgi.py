"""
WSGI config for unlimited_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

setting_file = os.environ.get('ENV', 'test')
print('wsgi settings:', setting_file)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.%s' % setting_file)

application = get_wsgi_application()

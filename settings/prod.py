from .base import *
import os


os.environ.setdefault('ENV', 'prod')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ywgsh_genesis_admin_prod_2',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'ywg_pss_root',
        'PASSWORD': 'ywgpss2020'
    }
}
# This file is part of e-Giełda.
# Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

"""
Django settings for egielda project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/
"""

import os

from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Security-related settings
DEBUG = True  # Don't run with True on production!
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = 'oi8%=kw9=ufj1g!jc1$ylxmvlk*7o8f=j_braal62(pj)z@m9f'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# General settings
SITE_NAME = "e-Giełda"
STATIC_URL = '/static/'

# Uploads
MEDIA_ROOT = 'upload/upload'
MEDIA_URL = '/static/upload/'
ALLOWED_UPLOAD_EXTS = ('PNG', 'JPG', 'JPEG')

# LDAP support
USE_LDAP_VERIFICATION = False
LDAP_SERVER_URL = None
LDAP_USERNAME = None
LDAP_PASS = None
LDAP_SEARCH_USER_PATH = None

# Internationalization
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'pl'
CURRENCY = 'zł'

TIME_ZONE = 'Europe/Warsaw'
USE_TZ = True

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Other settings
AUTH_USER_MODEL = 'authentication.AppUser'

INSTALLED_APPS = (
    'egielda',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'common',
    'authentication.apps.AuthenticationConfig',
    'books',
    'sell',
    'sellers',
    'purchase',
    'managemenu',
    'categories',
    'stats',
    'settings',
    'orders',
    'users',
    'utils',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'egielda.antibot.AntiBotMiddleware',
    'egielda.sellpurchaseavailable.SellPurchaseAvailableMiddleware',
    'egielda.cachelasturl.CacheLastURLMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "dist"),
    os.path.join(BASE_DIR, "upload"),
)

ROOT_URLCONF = 'egielda.urls'

WSGI_APPLICATION = 'egielda.wsgi.application'

LOGIN_REDIRECT_URL = 'egielda.views.home'

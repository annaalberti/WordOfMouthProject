"""
Django settings for a17 project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os, sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%$7yqc8&v5khx0z0__exl_)29xveqk1611c1z8wq3s1#t5*fps'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['https://a17-wordofmouth.herokuapp.com/', 'localhost', '127.0.0.1']
SECURE_SSL_REDIRECT = True

# Application definition

INSTALLED_APPS = [
    'wordofmouth.apps.WordofmouthConfig',
    'bootstrap5',
    'django.contrib.admin',
    'django.contrib.auth',
    'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gdstorage',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_bootstrap_icons',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SITE_ID = 3

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = BASE_DIR / 'google-drive-key.json'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'a17.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'a17.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

HEROKU_DATABASE = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'HOST': 'ec2-34-233-157-9.compute-1.amazonaws.com',
    'NAME': 'darhb2jamu3kv1',
    'USER': 'jzdabafqaflxzc',
    'PASSWORD': '97b88c100ad6907a0467fac910242f640f40eca3368ecd7ecfbd3c1162e82b7e',
    'PORT': '5432'
}

LOCAL_DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite3'
}
    
# Use local database if not on Heroku
if '/app' in os.environ['HOME']: DATABASES = { 'default': HEROKU_DATABASE }
else: DATABASES = {
    'default': LOCAL_DATABASE,
    'heroku': HEROKU_DATABASE
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
BS_ICONS_CUSTOM_PATH = 'wordofmouth/img'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

# Activate Django-Heroku.
try:
    if '/app' in os.environ['HOME']:
        import django_heroku
        django_heroku.settings(locals())
except ImportError:
    found = False

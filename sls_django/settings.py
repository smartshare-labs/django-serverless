"""
Django settings for sls_django project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "iyffqp!em_r^h@xtmow5^fgyk^a=tasl3me9qk-o#zl=h%391v"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "rest_framework",
    "sls_django.identity",
    "sls_django.pets",
]

args = sys.argv

if sys.argv[1] in ["migrate", "flush"] and sys.argv[-1] == "live":
    env_path = Path(".") / ".env_dev"  # TODO: support dev/prod environments
    load_dotenv(dotenv_path=env_path, verbose=True, override=True)
    del sys.argv[-1]
else:
    load_dotenv(override=True)


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": os.getenv("DB_PASS", "password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "35436"),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    "version": 1,
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler",},},
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "propagate": True,
            "level": "DEBUG",
        }
    },
}

from django.conf import settings
import django

INSTALLED_APPS = [
    "sls_django.example",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "slsdjango",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "35434",
    }
}


settings.configure(INSTALLED_APPS=INSTALLED_APPS, DATABASES=DATABASES)

# import models
django.setup()

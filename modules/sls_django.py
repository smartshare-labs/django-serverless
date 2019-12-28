from django.conf import settings
import django

from modules import parameters

INSTALLED_APPS = [
    "sls_django.example",
]

DB_CONFIG = parameters.from_config(
    ["DB_ENGINE", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
)

DATABASES = {
    "default": {
        "ENGINE": DB_CONFIG["DB_ENGINE"],
        "NAME": DB_CONFIG["DB_NAME"],
        "USER": DB_CONFIG["DB_USER"],
        "PASSWORD": DB_CONFIG["DB_PASSWORD"],
        "HOST": DB_CONFIG["DB_HOST"],
        "PORT": DB_CONFIG["DB_PORT"],
    }
}


settings.configure(INSTALLED_APPS=INSTALLED_APPS, DATABASES=DATABASES)
django.setup()

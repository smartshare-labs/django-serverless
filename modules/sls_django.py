from django.conf import settings
import django

from modules import parameters

INSTALLED_APPS = [
    "rest_framework",
    "rest_framework_gis",
    "sls_django.identity",
    "sls_django.threads",
]

DB_CONFIG = parameters.from_config(
    ["DB_ENGINE", "DB_NAME", "DB_USER", "DB_PASS", "DB_HOST", "DB_PORT"]
)

ADDITIONAL_CONFIG = parameters.from_config(["LIVE"])

DATABASES = {
    "default": {
        "ENGINE": DB_CONFIG["DB_ENGINE"],
        "NAME": DB_CONFIG["DB_NAME"],
        "USER": DB_CONFIG["DB_USER"],
        "PASSWORD": DB_CONFIG["DB_PASS"],
        "HOST": DB_CONFIG["DB_HOST"],
        "PORT": DB_CONFIG["DB_PORT"],
    }
}

# Add additional configuration options if running live
# TODO: clean this up
if ADDITIONAL_CONFIG["LIVE"] == "1":
    GDAL_LIBRARY_PATH = "/var/task/lib/libgdal.so.20.1.3"
    GEOS_LIBRARY_PATH = "/var/task/lib/libgeos_c.so.1"

    settings.configure(
        INSTALLED_APPS=INSTALLED_APPS,
        DATABASES=DATABASES,
        GDAL_LIBRARY_PATH=GDAL_LIBRARY_PATH,
        GEOS_LIBRARY_PATH=GEOS_LIBRARY_PATH,
    )
else:
    settings.configure(
        INSTALLED_APPS=INSTALLED_APPS, DATABASES=DATABASES,
    )

django.setup()

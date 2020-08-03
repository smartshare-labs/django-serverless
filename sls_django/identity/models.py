from datetime import datetime, timedelta
import os
import hashlib

from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from modules.utils import object_id


def six_months_from_now():
    d = timezone.now() + timedelta(days=365 / 2)
    return d


class AuthToken(models.Model):
    external_id = models.CharField(max_length=30, unique=True, default=object_id)
    key = models.CharField(max_length=255, unique=True)
    identity = models.ForeignKey("Identity", on_delete=models.PROTECT)
    expires = models.DateTimeField(default=six_months_from_now)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "identity_identity_authtoken"


def expire_authtokens(*, identity):
    AuthToken.objects.filter(identity=identity, expires__gte=timezone.now()).update(
        expires=timezone.now()
    )


def create_authtoken(identity):
    m = hashlib.sha512()

    m.update(str(identity.id).encode("utf-8"))
    m.update(str(identity.external_id).encode("utf-8"))
    m.update(str(datetime.now()).encode("utf-8"))
    m.update(os.urandom(32))

    return AuthToken.objects.create(key=m.hexdigest(), identity=identity)


class Identity(AbstractBaseUser):
    USERNAME_FIELD = "external_id"  # AbstractBaseUser customization

    external_id = models.CharField(max_length=30, unique=True, default=object_id)
    email = models.EmailField()

    class Meta:
        db_table = "identity_identity"

    def __str__(self):
        return f"{self.email}"


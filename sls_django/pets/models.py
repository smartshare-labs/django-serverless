from django.db import models

from modules import utils


class Pet(models.Model):
    external_id = models.CharField(max_length=30, unique=True, default=utils.object_id)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pets_pet"


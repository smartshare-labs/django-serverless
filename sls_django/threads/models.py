from django.db import models
from django.contrib.gis.db import models as geo_models

from modules import utils


class Thread(models.Model):
    external_id = models.CharField(max_length=30, unique=True, default=utils.object_id)

    started = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True)

    start_location = geo_models.PointField(null=True)
    end_location = geo_models.PointField(null=True)

    some_datetime = models.DateTimeField(auto_now=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "threads_thread"


class ThreadNode(models.Model):
    external_id = models.CharField(max_length=30, unique=True, default=utils.object_id)
    thread = models.ForeignKey(
        "threads.Thread", related_name="thread_node_thread", on_delete=models.PROTECT,
    )

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "threads_node"


class ThreadParameter(models.Model):
    external_id = models.CharField(max_length=30, unique=True, default=utils.object_id)
    thread = models.ForeignKey(
        "threads.Thread",
        related_name="thread_parameter_thread",
        on_delete=models.PROTECT,
    )

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "threads_parameter"


class ThreadParameterType(models.Model):
    external_id = models.CharField(max_length=30, unique=True, default=utils.object_id)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "threads_parameter_type"

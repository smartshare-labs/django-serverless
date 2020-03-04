import logging
from http import HTTPStatus

from modules import sls_django
from modules import cache
from modules import parameters
from modules import decorators


from sls_django.threads.models import Thread
from sls_django.threads.serializers import ThreadSerializer, TestSerializer


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_thread(thread_data):
    try:
        new_thread = Thread.objects.create(**thread_data)
    except Exception as e:
        logger.error(e)

    return new_thread


@decorators.serialized_handler(
    input_serializer=ThreadSerializer, output_serializer=TestSerializer, protected=True
)
def handler(event, context):
    body = {}
    body["echo"] = True

    return (body, HTTPStatus.OK)

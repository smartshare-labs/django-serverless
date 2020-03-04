import logging
from http import HTTPStatus

from modules import sls_django
from modules import cache
from modules import parameters
from modules import decorators

from sls_django.threads.models import Thread

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TODO: could make this handler take a serializer for input data
# and a serializer for output
@decorators.handler
def handler(event, context):
    body = {}
    body["echo"] = event.get("echo", None)
    return (body, HTTPStatus.OK)

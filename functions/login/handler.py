import logging
import json
from http import HTTPStatus

from modules import sls_django
from modules import cache
from modules import parameters
from modules import decorators

from sls_django.identity.serializers import LoginSerializer, OneTimeAuthTokenSerializer

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@decorators.serialized_handler(
    input_serializer=LoginSerializer, output_serializer=None,
)
def handler(event, context):
    token = event.get("token")
    body = {"token": token["key"]}
    return (body, HTTPStatus.OK)

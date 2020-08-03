import logging
import json

from http import HTTPStatus

from modules import sls_django
from modules import cache
from modules import parameters
from modules import decorators

from modules.actions import Actions

from sls_django.pets.models import Pet
from sls_django.identity.models import Identity

from sls_django.pets.serializers import (
    PetSerializer,
    ListPetSerializer
)
from logic import pets

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PetPermissions:
    protected = [
        Actions.ActionUpdate,
        Actions.ActionGeneric,
        Actions.ActionCreate,
    ]


@decorators.serialized_handler(
    input_serializer=PetSerializer,
    output_serializer=PetSerializer,
    permission_class=PetPermissions,
    allowed_actions=[
        Actions.ActionUpdate,
        Actions.ActionCreate,
        Actions.ActionRetrieve,
        Actions.ActionDelete,
        Actions.ActionList,
    ],
    action_serializers={
        Actions.ActionUpdate: PetSerializer,
        Actions.ActionCreate: PetSerializer,
        Actions.ActionList: ListPetSerializer,
        Actions.ActionRetrieve: ListPetSerializer,
    },
)
def handler(event, context):

    action = event.get("action")

    response = None
    status = None

    if action == Actions.ActionRetrieve:
        response = pets.get_pet(pet_id=event["pet_id"])
        status = HTTPStatus.OK

    elif action == Actions.ActionUpdate:
        response = pets.update_pet(
            pet_id=event.get("pet_id"),
            name=event.get("name")

        )
        status = HTTPStatus.OK

    elif action == Actions.ActionCreate:
        response = pets.create_pet(
            name=event.get("name"),
        )

        status = HTTPStatus.CREATED

    elif action == Actions.ActionDelete:
        response = pets.delete_pet(pet_id=event["pet_id"])
        status = HTTPStatus.NO_CONTENT

    elif action == Actions.ActionList:
        response = pets.list_pets()
        status = HTTPStatus.OK

    return (response, status)

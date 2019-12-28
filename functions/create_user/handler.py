import json
import logging

from modules import cache
from modules import parameters
from modules import sls_django

from sls_django.example.models import User

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_user(user_data):
    try:
        new_user = User.objects.create(**user_data)
    except Exception as e:
        print(e)
        # logger.info(f"user w/ email {email} does not exist.")
    return new_user


def handler(event, context):
    event_body = event.get("body", {})

    if isinstance(event_body, str):
        event_body = json.loads(event_body)

    body = {}
    new_user = None
    if event_body:
        new_user = create_user(event_body)

    body["new_user"] = {"email": new_user.email}
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response


if __name__ == "__main__":
    event = {"body": {}}

    with open("./test_events/create_user.json", "r") as f_in:
        event = json.loads(f_in.read())
        handler(event, {})

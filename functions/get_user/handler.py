import json
import logging

from modules import cache
from modules import parameters
from modules import sls_django

from sls_django.example.models import User

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_user(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        print("nope")
        logger.info(f"user w/ email {email} does not exist.")
    return user


def handler(event, context):
    event_body = event.get("body", {})

    if isinstance(event_body, str):
        event_body = json.loads(event_body)

    body = {}
    email = event_body.get("email")

    user = None
    if email:
        user = get_user(email)

    if user:
        body["user"] = {"email": user.email, "password": user.password}

    print(body)
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response


if __name__ == "__main__":
    event = {"body": {}}

    with open("./test_events/get_user.json", "r") as f_in:
        event = json.loads(f_in.read())
        handler(event, {})

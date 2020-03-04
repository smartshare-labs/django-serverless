import json

from rest_framework import serializers
from django.http import JsonResponse
from http import HTTPStatus

from modules.auth import validate_auth_token


def _parse_event_body(event):
    event_body = event.get("body", event)

    if isinstance(event_body, str):
        event_body = json.loads(event_body)
    elif not event_body:
        event_body = {}

    return event_body


def _parse_headers(event):
    event_headers = event.get("headers", {})

    if isinstance(event_headers, str):
        event_headers = json.loads(event_headers)
    elif not event_headers:
        event_headers = {}

    return event_headers


def _marshal(value):
    return json.dumps(json.loads(value))


def _bad_request(*, validation_error):
    return {
        "statusCode": HTTPStatus.BAD_REQUEST,
        "body": _marshal(validation_error),
    }


def _unauthenticated():
    return {"statusCode": HTTPStatus.UNAUTHORIZED, "body": json.dumps({})}


# naive handler; no serialization or auth
def handler(wrapped_handler):
    def _wrapper(*args, **kwargs):
        event = args[0]
        event_body = _parse_event_body(event)
        formatted_args = (event_body, args[1])  # args[1] is lambda event context

        response_body, status_code = wrapped_handler(*formatted_args, **kwargs)
        response = {"statusCode": status_code, "body": json.dumps(response_body)}

        return response

    return _wrapper


# includes input/output serialization as well as auth
def serialized_handler(*, input_serializer, output_serializer=None, protected=False):
    def _outer_wrapper(wrapped_handler):
        def _wrapper(*args, **kwargs):
            status_code = None
            identity = None

            event = args[0]

            event_body = _parse_event_body(event)
            event_headers = _parse_headers(event)

            # if protected, attempt to validate bearer token
            if protected:
                authenticated, identity = validate_auth_token(
                    event_headers.get("Authorization")
                )
                if not authenticated:
                    return _unauthenticated()

            # apply input serializer and save method (if implemented)
            try:
                serializer = input_serializer(data=event_body)
                serializer.is_valid(raise_exception=True)

                try:
                    event_body = serializer.save()
                except NotImplementedError:
                    event_body = serializer.data

                if identity:
                    event_body["identity"] = identity

                formatted_args = (
                    event_body,
                    args[1],  # args[1] is lambda event context
                )
                response_body, status_code = wrapped_handler(*formatted_args, **kwargs)

            except serializers.ValidationError as e:
                json_response = JsonResponse(e.__dict__, safe=False)
                return _bad_request(validation_error=json_response.content)

            # validation exceptions aren't caught here; they should be found during development
            if output_serializer:
                serializer = output_serializer(data=response_body)
                serializer.is_valid(raise_exception=True)

            response = {
                "statusCode": status_code,
                "body": json.dumps(response_body),
            }

            return response

        return _wrapper

    return _outer_wrapper

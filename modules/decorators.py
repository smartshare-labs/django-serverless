import json

from rest_framework import serializers
from django.http import JsonResponse
from django.db import connection
from http import HTTPStatus

from modules.auth import validate_auth_token
from modules.actions import Actions


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
        "headers": {"Access-Control-Allow-Origin": "*"},
    }


def _unauthenticated():
    return {
        "statusCode": HTTPStatus.UNAUTHORIZED,
        "body": json.dumps({}),
        "headers": {"Access-Control-Allow-Origin": "*"},
    }


def _action_not_permitted():
    return {
        "statusCode": HTTPStatus.METHOD_NOT_ALLOWED,
        "body": json.dumps({}),
        "headers": {"Access-Control-Allow-Origin": "*"},
    }


# naive handler; no serialization or auth
def handler(wrapped_handler):
    def _wrapper(*args, **kwargs):
        event = args[0]
        event_body = _parse_event_body(event)
        formatted_args = (event_body, args[1])  # args[1] is lambda event context

        response_body, status_code = wrapped_handler(*formatted_args, **kwargs)
        response = {
            "statusCode": status_code,
            "body": json.dumps(response_body),
            "headers": {"Access-Control-Allow-Origin": "*"},
        }

        return response

    # close database connections
    connection.close()

    return _wrapper


# includes input/output serialization as well as auth
def serialized_handler(
    input_serializer,
    output_serializer=None,
    permission_class=None,
    allowed_actions=[Actions.ActionGeneric],
    action_serializers={},
):
    def _outer_wrapper(wrapped_handler):
        def _wrapper(*args, **kwargs):
            serialize_to_use = input_serializer
            status_code = None
            identity = None

            event = args[0]

            event_body = _parse_event_body(event)
            event_headers = _parse_headers(event)

            action = event_body.get("action", Actions.ActionGeneric)
            if action not in allowed_actions:
                return _action_not_permitted()
            else:
                action_serializer = action_serializers.get(action, input_serializer)
                serialize_to_use = action_serializer

            # if protected, attempt to validate bearer token
            if permission_class and action in permission_class.protected:
                authenticated, identity = validate_auth_token(
                    event_headers.get("Authorization")
                )

                if not authenticated:
                    return _unauthenticated()

            # apply input serializer and save method (if implemented)
            try:
                serializer = serialize_to_use(data=event_body)
                serializer.is_valid(raise_exception=True)

                try:
                    serializer.save()
                    event_body = serializer.data
                except NotImplementedError:
                    event_body = serializer.data

                if identity:
                    event_body["identity"] = identity

                event_body[
                    "action"
                ] = action  # TODO: build this into context instead probably
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

                if isinstance(response_body, list):
                    serializer = output_serializer(response_body, many=True)
                else:
                    serializer = output_serializer(response_body)

                # serializer.is_valid(raise_exception=True) # TODO: validate this shit
                response_body = serializer.data

            response = {
                "statusCode": status_code,
                "body": json.dumps(response_body),
                "headers": {"Access-Control-Allow-Origin": "*"},
            }

            # close database connections
            connection.close()

            return response

        return _wrapper

    return _outer_wrapper

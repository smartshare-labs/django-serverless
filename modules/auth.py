from sls_django.identity.models import AuthToken, Identity
from django.utils import timezone


def validate_auth_token(token):
    try:
        key = token.split(" ")[-1]
    except:
        return False, None

    try:
        auth_token = AuthToken.objects.get(key=key, expires__gte=timezone.now())
    except AuthToken.DoesNotExist:
        return False, None

    return True, auth_token.identity

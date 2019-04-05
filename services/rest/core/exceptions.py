from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException


class CredentialException(APIException):
    status_code = 401
    default_detail = 'Bad credentials: Check your Github API credentials'
    default_code = 'credential_error'


class ConnectionException(APIException):
    status_code = 503
    default_detail = 'Service Unavailable: max retries exceeded'
    default_code = 'connection_error'


class TimeoutException(APIException):
    status_code = 504
    default_detail = 'Gateway Timeout: Unable to reach GITHUB API'
    default_code = 'connection_error'

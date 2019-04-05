"""
Some module comments
"""

import json
import hashlib
from typing import Dict, List

import redis
from django.utils.translation import ugettext_lazy as _
from rest_framework import status, views
from rest_framework.exceptions import APIException

from app.settings import CORE_REST_SETTINGS


def url_composer(url_parts: List) -> str:
    return '/'.join(map(str, url_parts))

#
# def get_auth(user: str, password: str) -> requests.auth.HTTPBasicAuth:
#     auth = requests.auth.HTTPBasicAuth(
#         username='',
#         password=''
#     )
#     return auth
#


class ConnectionErrorException(APIException):
    status_code = 503
    default_detail = _('Service Unavailable (connection error): max retries exceeded')
    default_code = 'connection_error'


class TimeoutErrorException(APIException):
    status_code = 504
    default_detail = _('Gateway Timeout: Unable to reach GITHUB API')
    default_code = 'connection_error'


def get_fields(repo_data: Dict, repo_fields: Dict) -> Dict:
    """
    Helper function responsible for selection proprietary fields from repo_data param and handling name transition
    from snake_case to camelCase

    :param repo_data: Initial data to be filtered
    :type repo_data: Dict
    :param repo_fields: Filters and transition fields
    :type repo_fields: Dict
    :return: Data with proprietary fields
    :rtype: Dict
    """
    # Python dictionary comprehension for filtering and handling field names transition in one step
    return {repo_fields[key]: value for key, value in repo_data.items() if key in repo_fields.keys()}


def custom_exception_handler(exception, context):
    # Call REST framework's default exception handler first, to get the standard error response.
    response = views.exception_handler(exception, context)
    # Update and add proprietary response data fields
    response.data.update({
        'message': exception.detail,
        'documentation_url': CORE_REST_SETTINGS['DOCUMENTATION_URL'],
    })
    # Remove redundant detail field from predefined DRF response
    del response.data['detail']
    # Set "Not Found" msg and 404 status code for all requests directed to inappropriate endpoints
    if str(context['view']) == 'default':
        response.data['message'] = 'Not Found'
        response.status_code = 404
    return response


def set_cache(key, value, r_conn, ex_time_secs):
    hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
    json_value = json.dumps(value)
    try:
        r_conn.set(name=hash_key, value=json_value, ex=ex_time_secs)
    except redis.ConnectionError:
        pass  # TODO there is no way to get Redis, logging to file


def get_cache(key, redis_conn):
    hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
    try:
        redis_value = redis_conn.get(hash_key)
    except redis.ConnectionError:
        # TODO: logging connection error, there is no way to get redis
        print('Redis dont work')
        return None
    else:
        if redis_value:  # It will be set to None if there is no key in redis
            print('OK there is a key i am going to return appropriate value')
            return json.loads(redis_value)
        else:
            print('OK no key i am going to return None')
            return redis_value  # It will be set to None if there is no key in redis

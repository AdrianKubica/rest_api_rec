"""
SOME modeule description
"""

import hashlib
import json
import logging
from typing import Dict, List

import redis
from requests.auth import HTTPBasicAuth
from rest_framework import views
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.settings import CORE_REST_SETTINGS

logger = logging.getLogger(__name__)


def url_composer(url_parts: List) -> str:
    """
    Helper function concatenates strings with '/' character, similar to urllib.parse.urljoin
    but this one is able to concatenate more items and dont expect only urls

    :param url_parts: List of items (numbers or strings) to be concatenated
    :type url_parts: List of numbers or strings
    :return: String with slashes for delivered list
    :rtype: str
    """
    return '/'.join(map(str, url_parts))


def get_auth() -> HTTPBasicAuth:
    """
    Helper function creates HTTPBasicAuth object for requests library authentication

    :return: Requests library HTTPBasicAuth object
    :rtype: HTTPBasicAuth
    """
    # Create HTTBasicAuth object from requests library
    auth = HTTPBasicAuth(username=CORE_REST_SETTINGS['CREDENTIALS']['USER_NAME'],
                         password=CORE_REST_SETTINGS['CREDENTIALS']['USER_PASSWORD'])
    return auth


def get_fields(repo_data: Dict, repo_fields: Dict) -> Dict:
    """
    Helper function selects proprietary fields from repo_data param and handling name transition
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


def set_cache(key: str, value: Dict, redis_conn: redis.Redis, ex_time_secs: int) -> None:
    """
    Helper function hashes 'key' with sha256 and tries to save 'value' under that hash in Redis Cache.
    This value expires after 'ex_time_secs' seconds

    :param key: String value for hash function and key identifier in Redis Cache
    :type key: str
    :param value: Dictionary for JSON serialization and data to be stored in Redis Cache
    :param redis_conn: Redis connection instance
    :type redis_conn: redis.Redis
    :param ex_time_secs: Time interval which stands for key expiration in seconds
    :type ex_time_secs: int
    :return: Dict
    :rtype: None
    """
    # Get key hash value for use as Redis key identifier
    hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
    # Serialize data to JSON format
    json_value = json.dumps(value)
    try:
        # Try to set identifier and serialized data in Redis cache with
        redis_conn.set(name=hash_key, value=json_value, ex=ex_time_secs)
    except redis.ConnectionError:
        # Log custom error message if Redis is unreachable
        logger.error('[SET CACHE] Connection error: Redis cache unreachable')


def get_cache(key: str, redis_conn: redis.Redis) -> bool:
    # Get key hash value for use as Redis key identifier
    hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
    try:
        # Try to get data for hash value from Redis cache
        redis_value = redis_conn.get(hash_key)
    except redis.ConnectionError:
        # Log custom error message if Redis is unreachable and set False as function result
        logger.error('[GET CACHE] Connection error: Redis cache unreachable')
        return False
    else:
        if redis_value:  # It will be set to None if there is no key in redis
            # Log custom message
            logger.info('[CACHED VALUE] Appropriate value returned from Redis cache')
            return json.loads(redis_value)
        else:
            logger.info('[NO CACHED VALUE] No appropriate value to return from Redis cache, hit Github API')
            return redis_value  # It will be set to None if there is no key in redis


def custom_exception_handler(exception: APIException, context: Dict) -> Response:
    # Call REST framework's default exception handler first, to get the standard error response.
    response = views.exception_handler(exception, context)
    # Update and add documentation_url data field for clients response
    # print(exception)
    response.data = {
        'message': exception.detail,
        'documentation_url': CORE_REST_SETTINGS['DOCUMENTATION_URL'],
    }
    # TODO: czy dodawać do cache błędne odpowiedzi, co z cache dla credential error
    # Catch all requests to inappropriate endpoints (directed to "DefaultView") and set 404 status code
    # with "Not Found" message
    if repr(context['view']) == 'default':
        response.status_code = 404
        response.data['message'] = 'Not Found'
    return response

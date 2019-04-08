"""
Utils module contains helper functions for core application such as:
    - user authentication,
    - data filtering,
    - custom error handler
"""

import logging
from typing import Dict

from requests.auth import HTTPBasicAuth
from rest_framework import views
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.settings import CORE_REST_SETTINGS

logger = logging.getLogger(__name__)


def get_auth() -> HTTPBasicAuth:
    """
    Helper function creates HTTPBasicAuth object for requests library authentication.
    You can extend this method in the future to support other forms of authentication.

    :return: Requests library HTTPBasicAuth object
    :rtype: HTTPBasicAuth
    """
    # Create HTTBasicAuth object from requests library to support authentication
    auth = HTTPBasicAuth(username=CORE_REST_SETTINGS['CREDENTIALS']['USER_NAME'],
                         password=CORE_REST_SETTINGS['CREDENTIALS']['USER_PASSWORD'])
    return auth


def get_fields(repo_data: Dict, repo_fields: Dict) -> Dict:
    """
    Helper function selects proprietary fields from repo_data param and handles simple name transition
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


def custom_exception_handler(exception: APIException, context: Dict) -> Response:
    """
    Exception handler for all errors raised by Django Rest Framework. This function captures all errors
    from each endpoint of application.

    :param exception: APIException error captured by Django Rest Framework
    :type exception: Dict
    :param context: Context with information's about view which raised an error and context variables.
    :type context: Dict
    :return: Response data for client application
    :rtype: Dict
    """
    # Call framework's default exception_handler function to get information's about error response data
    response = views.exception_handler(exception, context)
    # Update and add documentation_url field to client response
    response.data = {
        'message': exception.default_detail,
        'documentation_url': CORE_REST_SETTINGS['DOCUMENTATION_URL'],
    }
    return response

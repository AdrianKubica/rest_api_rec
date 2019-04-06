"""
SOME modeule description
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


def custom_exception_handler(exception: APIException, context: Dict) -> Response:
    # Call REST framework's default exception handler first, to get the standard error response.
    response = views.exception_handler(exception, context)
    # Update and add documentation_url data field for clients response
    response.data = {
        'message': exception.default_detail,
        'documentation_url': CORE_REST_SETTINGS['DOCUMENTATION_URL'],
    }
    # Catch all requests to inappropriate endpoints (directed to "DefaultView") and set 404 status code
    # with "Not Found" message
    if str(context['view']) == 'default':
        response.status_code = 404
        response.data['message'] = 'Not Found'
    return response

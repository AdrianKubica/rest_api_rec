from typing import Dict, List

import requests
from rest_framework import views


def url_composer(url_parts: List) -> str:
    return '/'.join(map(str, url_parts))


def get_auth(user: str, password: str) -> requests.auth.HTTPBasicAuth:
    auth = requests.auth.HTTPBasicAuth(
        username='',
        password=''
    )
    return auth


def get_fields(repo_data: Dict, repo_fields: Dict) -> Dict:
    """
    Helper function responsible for selection proprietary fields from
    repo_data param and name transition from snake_case to camelCase

    :param repo_data: Initial data to be filtered
    :type repo_data: Dict
    :param repo_fields: Filters and transition fields
    :type repo_fields: Dict
    :return: Data with proprietary fields
    :rtype: Dict
    """
    # Python dictionary comprehension to filter and handle
    # fields name transition in one step
    return {
        repo_fields[key]: value for key, value in repo_data.items()
        if key in repo_fields.keys()
    }


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = views.exception_handler(exc, context)
    # Update and add proprietary response data fields
    response.data.update({
        'message': exc.detail,
        'documentation_url': 'https://github.com/AdrianKubica/rest_api_rec',
    })
    # Remove redundant detail field
    del response.data['detail']
    # Set "Not Found" msg and 404 status code
    # for all requests directed to inappropriate endpoints
    if repr(context['view']) == 'default':
        response.data['message'] = 'Not found.'
        response.status_code = 404
    return response

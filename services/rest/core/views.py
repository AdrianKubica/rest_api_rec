"""
This module handles HTTP methods for REST API. Currently there is only one HTTP GET method allowed, which stands for
read-only access for all endpoints of this application.

"""

import logging

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError, Timeout
from rest_framework import views, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response

from app.settings import CORE_REST_SETTINGS
from core.serializers import UserRepoSerializer
from core.utils import get_fields, get_auth

CACHE_TTL = getattr(settings, 'CACHE_TTL')

logger = logging.getLogger(__name__)


class UserRepoView(views.APIView):
    """
    UserRepoView handles each request directed to endpoint:

    /repositories/{owner}/{repo_name}

    """
    serializer_class: UserRepoSerializer = UserRepoSerializer

    @method_decorator(cache_page(CACHE_TTL))  # set cache for this method responses
    @method_decorator(vary_on_cookie)  # for security reason sticks cache to appropriate session
    def get(self, request: Request, owner: str, repo_name: str) -> Response:
        """
        UserRepoView "GET" method handles HTTP GET request and return Django Rest Framework (application/json MIME type)
        response to client

        :param request: Client HTTP request directed to UserRepoView
        :type request: Request object
        :param owner: Stands for owner repository we are interesting in
        :type owner: str
        :param repo_name: Stands for repository name we are looking for
        :type repo_name: str
        :return: Django Rest Framework Response object with data from Github API. This response is send back to client
        application
        :rtype: Django Rest Framework Response
        """

        # Create session adapter with retry connection attribute
        http_adapter = HTTPAdapter(max_retries=3)

        # Open requests library session to keep persistent connection
        with Session() as session:
            # Mount http_adapter for Github API
            session.mount('https://api.github.com', http_adapter)
            # Get authenticated session
            session.auth = get_auth()
            # According to Github API explicitly choose API version, keep in mind that in the future API can be changed
            session.headers.update({'Accept': 'application/vnd.github.v3+json'})
            # Create Github API url for GET method
            url = f'{CORE_REST_SETTINGS["GITHUB_URL"]}/{owner}/{repo_name}'

            # By default, requests do not time out unless a timeout value is set explicitly. Without a timeout,
            # code may hang for minutes or more, so set connection timeout interval
            try:
                # Save request results to "res" variable which stands for response data and take care about timeout
                # attribute
                res = session.get(url, timeout=3)
                # Raise error if there is such error status code
                res.raise_for_status()
            except HTTPError:
                # Log error information's to console
                logger.error(f'[Status code: {res.status_code}] {res.json()["message"]}')
                # Dynamic error class instantiation which forwarding Github status code and message
                # to custom_exception_handler
                raise type('CustomHTTPError', (APIException,), {
                    'status_code': res.status_code,
                    'default_detail': res.json()['message'],
                })
            except ConnectionError:
                # Log error information's to console
                logger.error('[Status code: 503] Service Unavailable: max retries exceeded')
                # Dynamic error class instantiation which forwarding Github status code and message
                # to custom_exception_handler
                raise type('CustomConnectionError', (APIException,), {
                    'status_code': 503,
                    'default_detail': 'Service Unavailable: max retries exceeded',
                })
            except Timeout:
                # Log error information's to console
                logger.error('[Status code: 504] Timeout Error: Unable to reach GITHUB API')
                # Dynamic error class instantiation which forwarding Github status code and message
                # to custom_exception_handler
                raise type('CustomTimeoutError', (APIException,), {
                    'status_code': 504,
                    'default_detail': '[Status code: 504] Timeout Error: Unable to reach GITHUB API',
                })
            else:
                # Filter response data and fetch only interesting fields according to REST_SETTINGS configuration
                # from settings.py
                repo_data = get_fields(res.json(), CORE_REST_SETTINGS['REPO_FIELDS'])

                # Create serializer for selected data
                serializer = UserRepoSerializer(repo_data)
                return Response(serializer.data)


@api_view()
def not_found(request: Request) -> Response:
    """
    This view handles each request which is not directed for any other view in application. Its responsible for
    returning user friendly Not Found message in JSON format and 404 HTTP status code.

    :param request: Client HTTP request directed to not_found API view
    :type request: Request object
    :return: Django Rest Framework Response object with predefined data for 404 Not Found Error. This response is
    send back to client application.
    :rtype: Django Rest Framework Response
    """

    return Response({'message': 'Not found', 'documentation_url': CORE_REST_SETTINGS['DOCUMENTATION_URL']},
                    status=status.HTTP_404_NOT_FOUND)

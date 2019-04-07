"""
Some module comments
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
    UserRepoView handles each request directed to endpoint '/repositories/<owner>/<repo_name>
    """
    serializer_class: UserRepoSerializer = UserRepoSerializer

    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)  # for security reasons stick cache to appropriate session
    def get(self, request: Request, owner: str, repo_name: str) -> Response:
        """
        UserRepoView get method handles HTTP GET request and return DRF (application/json) response to client

        :param request: Client HTTP request directed to UserRepoView
        :type request: Request object
        :param owner: Stands for owner repository we are interesting in
        :type owner: str
        :param repo_name: Stands for repository name we are looking for
        :type repo_name: str
        :return: DRF Response object with data from Github API. This response is send back to client application
        :rtype: DRF Response
        """
        logger.error('You hit github api')

        # Create session adapter with retry connection attribute0
        http_adapter = HTTPAdapter(max_retries=3)

        # Open requests library session to keep persistent connection
        with Session() as session:
            # Mounting http_adapter for Github API
            session.mount('https://api.github.com', http_adapter)
            # Get authenticated session
            session.auth = get_auth()
            # According to Github API explicitly choose API version, it can be changed in the future
            session.headers.update({'Accept': 'application/vnd.github.v3+json'})
            # Create Github API url for GET method
            url = f'{CORE_REST_SETTINGS["GITHUB_URL"]}/{owner}/{repo_name}'

            # By default, requests do not time out unless a timeout value is set explicitly. Without a timeout,
            # code may hang for minutes or more, so set connection timeout
            try:
                # Save request results to "res" which stands for response data and take care about timeout attribute
                res = session.get(url, timeout=3)
                res.raise_for_status()
            except HTTPError:
                logger.error(f'[Status code: {res.status_code}] {res.json()["message"]}')
                # Dynamic class instantiation with "type" for forwarding Github status code and message
                raise type('CustomHTTPError', (APIException,), {
                    'status_code': res.status_code,
                    'default_detail': res.json()['message'],
                })
            except ConnectionError:
                logger.error('[Status code: 503] Service Unavailable: max retries exceeded')
                # Dynamic class instantiation with "type" for ConnectionError
                raise type('CustomConnectionError', (APIException,), {
                    'status_code': 503,
                    'default_detail': 'Service Unavailable: max retries exceeded',
                })
            except Timeout:
                logger.error('[Status code: 504] Timeout Error: Unable to reach GITHUB API')
                # Dynamic class instantiation with "type" for TimeoutError
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
def other_endpoint(request):
    return Response({'message': 'Not found', 'documentation_url': CORE_REST_SETTINGS['DOCUMENTATION_URL']},
                    status=status.HTTP_404_NOT_FOUND)

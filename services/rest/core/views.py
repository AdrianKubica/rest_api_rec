"""
Some module comments
"""

import redis
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError, Timeout
from rest_framework import views
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from app.settings import CORE_REST_SETTINGS
from core.serializers import UserRepoSerializer
from core.utils import get_fields, url_composer, ConnectionErrorException, TimeoutErrorException, set_cache, get_cache

# Connect to Redis instance
redis_conn = redis.Redis(host=CORE_REST_SETTINGS['redis']['HOST'], port=CORE_REST_SETTINGS['redis']['PORT'], db=0)


class UserRepoView(views.APIView):
    serializer_class = UserRepoSerializer

    def get(self, request, owner, repo):
        """
        Some comment for method
        """
        # Trying to get repo data from redis cache
        repo_data = get_cache(owner + repo, redis_conn)
        # If there is no value in cache which stands for "None" then try to pull it from Github API
        if repo_data is None:
            print('You hit the Github API')
            # Create session adapter with retry connection attribute
            http_adapter = HTTPAdapter(max_retries=3)

            # Open requests library session to keep persistent connection
            with Session() as session:
                # TODO: session headers according to Github API docs
                # Mounting http_adapter for Github API
                session.mount('https://api.github.com', http_adapter)

                # Create Github API url for GET method
                url = url_composer([CORE_REST_SETTINGS['github_url'], owner, repo])

                # By default, requests do not time out unless a timeout value is set explicitly. Without a timeout,
                # code may hang for minutes or more, so set connection timeout
                try:
                    # Save request results to "res" which stands for response data and take care about timeout attribute
                    res = session.get(url, timeout=3.05)
                    res.raise_for_status()
                except HTTPError:
                    if res.status_code == 404:
                        raise NotFound
                    # tutaj jeszcze rzucic ten blad http
                    # TODO: obsługa pozostałych błędów
                except ConnectionError:
                    # TODO: logging info to file
                    raise ConnectionErrorException
                except Timeout:
                    # TODO: logging info
                    raise TimeoutErrorException
                else:
                    # Filter response data and fetch only interesting fields according to REST_SETTINGS configuration
                    # from settings.py
                    repo_data = get_fields(res.json(), CORE_REST_SETTINGS['repo_fields'])

        # Create serializer for selected data
        serializer = UserRepoSerializer(repo_data)
        # SET redis cache to protect internet badwith
        set_cache(owner + repo, serializer.data, redis_conn, CORE_REST_SETTINGS['redis']['redis_cache_time'])
        return Response(serializer.data)


class DefaultView(views.APIView):
    # Core REST API errors are handled by core.utils.custom_exception_handler. If error occurs and exception context
    # handler is set to "default" then 404 Not Found response is generated. There is no need to make requests
    # to GithubAPI if Core REST API gets inappropriate url in request
    def __repr__(self):
        return 'default'

"""
Some module comments
"""

import requests
from rest_framework import views
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from app.settings import REST_SETTINGS
from core.serializers import UserRepoSerializer
from core.utils import get_fields, url_composer


class UserRepoView(views.APIView):
    serializer_class = UserRepoSerializer

    def get(self, request, owner, repo):
        """
        Some comment for method
        """
        # Open requests library session
        with requests.Session() as session:
            # Create Github API url for GET method
            url = url_composer([REST_SETTINGS['github_url'], owner, repo])
            # Save request results to "res" which stands for response data
            res = session.get(url)
            if res.status_code == 404:
                raise NotFound
        # Filter response data and fetch only interesting
        # fields according to REST_SETTINGS configuration
        repo_data = get_fields(res.json(), REST_SETTINGS['repo_fields'])
        # Create serializer for selected data
        import pdb; pdb.set_trace()
        serializer = UserRepoSerializer(repo_data)
        return Response(serializer.data)


class DefaultView(views.APIView):
    # API errors are handled by core.utils.custom_exception_handler
    def __repr__(self):
        return 'default'

import json
from unittest.mock import Mock, MagicMock

import pytest
import requests
from requests import Session, Response
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from core.views import UserRepoView, DefaultView


class ResponseMock(Response):
    def __init__(self, status_code, result, expected):
        self.status_code = status_code
        self.result = result
        self.expected = expected
        self.reason = ''
        self.url = ''

    def json(self):
        return self.result

    def raise_for_status(self):
        super().raise_for_status()


class RequestMock(Request):
    def __init__(self):
        self.method = None


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture(params=[
    (200, {'a': 10, 'b': 20}, b'{}'),
    (200, {
        'full_name': 'John',
        'description': 'Some interesting API',
        'clone_url': 'http://api.github.com/repos/jan/some_project',
        'stargazers_count': 55,
        'created_at': '2011-02-13T18:38:17Z',
        'field_to_be_deleted': 'test_data'
        },
        json.dumps({
         'fullName': 'John',
         'description': 'Some interesting API',
         'cloneUrl': 'http://api.github.com/repos/jan/some_project',
         'stars': 55,
         'createdAt': '2011-02-13T18:38:17Z'
        }, separators=(',', ':')).encode('utf-8'),
     ),
    (404, {'message': ''}, b'{}'),
])
def response_mock(request):
    """
    :param param[0]: Stands for HTTP status code
    :param param[1]: Stands for results of data res.json() call
    :param param[2]: Stands for expected data

    :param request: Stands for pytest fixture
    """
    response_mock = ResponseMock(
        request.param[0],
        request.param[1],
        request.param[2]
    )
    return response_mock


@pytest.mark.parametrize('owner, repo_name', (
        ('john', 'some_project'),
))
def test_user_repo_view_get(owner, repo_name, response_mock):
    Session.get = Mock()
    Session.get.return_value = response_mock

    if response_mock.status_code == 404:
        with pytest.raises((requests.HTTPError, APIException)):
            UserRepoView().get(RequestMock(), owner, repo_name)
    else:
        response = UserRepoView().get(RequestMock(), owner, repo_name)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        assert response.content == response_mock.expected


def test_default_view():
    assert repr(DefaultView()) == 'default'

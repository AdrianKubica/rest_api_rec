from unittest.mock import Mock

import pytest
from requests import Session
from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer

from core.views import UserRepoView


class RequestsResponseMock:
    def __init__(self, status_code, result, expected):
        self.status_code = status_code
        self.result = result
        self.expected = expected

    def json(self):
        return self.result


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture(params=[
    (200, {'a': 10, 'b': 20}, b'{}'),
    (200, {'d': 20}, b'{"a": 2}'),
    (404, {'d': 20}, {}),
])
def response_mock(request):
    """
    :param param[0]: Stands for HTTP status code
    :param param[1]: Stands for results of data res.json() call
    :param param[2]: Stands for expected data

    :param request: Stands for pytest fixture
    """
    response_mock = RequestsResponseMock(
        request.param[0],
        request.param[1],
        request.param[2]
    )
    return response_mock


@pytest.mark.parametrize('url_request, owner, repo', (
        ('url_request', 'jan', 'jan_repo'),
))
def test_user_repo_view_get(url_request, owner, repo, response_mock):
    Session.get = Mock()
    Session.get.return_value = response_mock

    if response_mock.status_code == 404:
        with pytest.raises(NotFound):
            UserRepoView().get(url_request, owner, repo)
    else:
        response = UserRepoView().get(url_request, owner, repo)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        assert response.content == response_mock.expected


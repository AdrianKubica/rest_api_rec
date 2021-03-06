import json
from unittest.mock import Mock

import pytest
import requests
from django.test import RequestFactory
from requests import Session, Response
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from app.settings import CORE_REST_SETTINGS
from core.views import UserRepoView, not_found


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """This fixture switch off possibilities to send requests by requests library"""
    monkeypatch.delattr('requests.sessions.Session.request')


class ResponseMock(Response):
    """This class is responsible for mocking response object from Session.get used in views.UserRepoView.get method"""
    def __init__(self, status_code, result, expected, raise_error=None):
        super().__init__()
        self.status_code = status_code
        self.result = result
        self.expected = expected
        self.raise_error = raise_error
        self.reason = ''
        self.url = ''

    def json(self):
        """This method imitates response.json() method from requests library"""
        return self.result

    def raise_for_status(self):
        """This method imitates response.raise_for_status() method from requests library. If self.raise_error is set
        to some Error Class it can raise proper Exception. This allows to test for example ConnectionError
        and Timeout Error"""
        if self.raise_error:
            raise self.raise_error
        super().raise_for_status()


class RequestMock(Request):
    """This class imitates Request object when testing views.UserRepoView.get method"""
    def __init__(self):
        self.method = ''


@pytest.fixture(params=[
    (200, {'a': 10, 'b': 20}, b'{}', None),
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
     None
     ),
    (404, {'message': ''}, b'{}', None),
    (503, {'message': ''}, b'{}', requests.ConnectionError),
    (504, {'message': ''}, b'{}', requests.Timeout),
])
def response_mock(request):
    """
    This fixtures parametrize ResponseMock object when testing views.UserRepoView.get method

    :param param[0]: Stands for HTTP status code
    :param param[1]: Stands for results of data res.json() call
    :param param[2]: Stands for expected data
    :param param[3]: Stands for raising specified errors

    :param request: Stands for pytest fixture
    """
    response_mock = ResponseMock(request.param[0], request.param[1], request.param[2], request.param[3])
    return response_mock


@pytest.mark.parametrize('owner, repo_name', (
        ('john', 'some_project'),
))
def test_user_repo_view_get(owner, repo_name, response_mock):
    """
    This function tests views.UserRepoView.get method for each parameters declared above with ResponseMock()
    and RequestMock() objects
    """
    Session.get = Mock()
    Session.get.return_value = response_mock

    if response_mock.status_code == 404:
        with pytest.raises((requests.HTTPError, APIException)):
            UserRepoView().get(RequestMock(), owner, repo_name)
    elif response_mock.status_code == 503:
        with pytest.raises((requests.ConnectionError, APIException)):
            UserRepoView().get(RequestMock(), owner, repo_name)
    elif response_mock.status_code == 504:
        with pytest.raises((requests.Timeout, APIException)):
            UserRepoView().get(RequestMock(), owner, repo_name)
    else:
        response = UserRepoView().get(RequestMock(), owner, repo_name)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        assert response.content == response_mock.expected


def test_other_endpoint_view():
    """
    This function tests if not_found view returns proper format of response.data with 'message'
    and 'documentation_url' keys
    """
    request_factory = RequestFactory()
    request = request_factory.get('/path', data={'name': u'test'})
    response = not_found(request)
    assert response.data == {'message': 'Not found', 'documentation_url': CORE_REST_SETTINGS['DOCUMENTATION_URL']}

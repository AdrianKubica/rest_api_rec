from unittest.mock import Mock

import pytest
from rest_framework import views

from app.settings import REST_SETTINGS
from core.utils import get_fields, url_composer, custom_exception_handler


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.mark.parametrize('url_parts, expected', (
    (
        ['https://api/github.com', 'first', 'second'],
        'https://api/github.com/first/second'
    ),
    ([1, 2, 3, 4, 5], '1/2/3/4/5'),
    ([], ''),
))
def test_url_composer(url_parts, expected):
    url = url_composer(url_parts)
    assert url == expected


@pytest.mark.parametrize('repo_data, repo_fields, expected', (
    ({'a': 10, 'b': 20}, {'a': 'c', 'b': 'd'}, {'c': 10, 'd': 20}),
    ({'a': 10, 'b': 20}, {'a': 'c'}, {'c': 10}),
    ({'a': 10, 'b': 20, 'c': 30}, {'a': 'c', 'b': 'd'}, {'c': 10, 'd': 20}),
    ({}, {'a': 'c'}, {}),
    ({'a': 10, 'b': 20}, {}, {}),
))
def test_get_fields(repo_data, repo_fields, expected):
    filtered_data = get_fields(repo_data, repo_fields)
    assert filtered_data == expected


class ExceptionHandlerMock:
    def __init__(self, load_attr):
        self.__dict__.update(load_attr)


class ExceptionMock:
    def __init__(self, load_attr):
        self.__dict__.update(load_attr)

    def __getitem__(self, item):
        return self.__dict__[item]


@pytest.fixture(params=[
    {
        'data': {'detail': 10},
        'exception': ExceptionMock({'detail': {'New content'}}),
        'context': ExceptionMock({'view': 'default'}),
        'expected': {
            'data': {
                'message': 'Not Found',
                'documentation_url': REST_SETTINGS['documentation_url']
            }, 'status_code': 404
        }
    },
])
def exc_handler_mock(request):
    exc_handler_mock = ExceptionHandlerMock(request.param)
    return exc_handler_mock


def test_custom_exception_handler(exc_handler_mock):
    views.exception_handler = Mock()
    views.exception_handler.return_value = exc_handler_mock

    response = custom_exception_handler(
        exc_handler_mock.exception,
        exc_handler_mock.context
    )

    assert response.data == exc_handler_mock.expected['data']
    assert response.status_code == exc_handler_mock.expected['status_code']
    assert not hasattr(response, 'detail')

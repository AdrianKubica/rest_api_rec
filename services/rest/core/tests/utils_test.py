from unittest.mock import Mock

import pytest
from rest_framework import views

from app.settings import CORE_REST_SETTINGS
from core.utils import get_fields, custom_exception_handler


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """This fixture switch off possibilities to send requests by requests library"""
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.mark.parametrize('repo_data, repo_fields, expected', (
    ({'a': 10, 'b': 20}, {'a': 'c', 'b': 'd'}, {'c': 10, 'd': 20}),
    ({'a': 10, 'b': 20}, {'a': 'c'}, {'c': 10}),
    ({'a': 10, 'b': 20, 'c': 30}, {'a': 'c', 'b': 'd'}, {'c': 10, 'd': 20}),
    ({}, {'a': 'c'}, {}),
    ({'a': 10, 'b': 20}, {}, {}),
))
def test_get_fields(repo_data, repo_fields, expected):
    """This function tests if get_fields helper function makes proper fields transition for dict inputs"""
    filtered_data = get_fields(repo_data, repo_fields)
    assert filtered_data == expected


class ExceptionMock:
    """
    This is Exception Mock class for testing custom_exception_handler function. This function is used for capturing
    exceptions in REST API
    """
    def __init__(self, load_attr):
        self.__dict__.update(load_attr)

    def __getitem__(self, item):
        return self.__dict__[item]


@pytest.fixture(params=[
    {
        'data': {'detail': 10},
        'exception': ExceptionMock({'default_detail': 'New content'}),
        'context': ExceptionMock({'view': 'not default'}),
        'expected': {
            'data': {
                'message': 'New content',
                'documentation_url': CORE_REST_SETTINGS['DOCUMENTATION_URL']
            }
        },
    },
])
def exc_handler_mock(request):
    """This fixture is responsible for instantiation ExceptionMock class with testing parameters"""
    exc_handler_mock = ExceptionMock(request.param)
    return exc_handler_mock


def test_custom_exception_handler(exc_handler_mock):
    """
    This function tests custom_exception_handler function and uses parametrized fixture object from
    exc_handler_mock. Function checks if returned values (exception.default_detail) match expected values and also if
    response object has appropriate keys such as: 'message' and 'documentation_url'.
    """
    views.exception_handler = Mock()
    views.exception_handler.return_value = exc_handler_mock

    response = custom_exception_handler(exc_handler_mock.exception, exc_handler_mock.context)

    assert response.data == exc_handler_mock['expected']['data']
    assert 'message' in response.data.keys()
    assert 'documentation_url' in response.data.keys()

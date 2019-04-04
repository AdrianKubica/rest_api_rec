import pytest

from core.utils import get_fields, url_composer


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

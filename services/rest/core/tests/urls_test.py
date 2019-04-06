from django.urls import resolve, reverse

import pytest


@pytest.mark.parametrize('url_name, args, expected', (
    ('repo', ['john', 'john_repo'], '/repositories/john/john_repo'),
    ('default', None, '/'),
))
def test_urls(url_name, args, expected):
    url = reverse(url_name, args=args)
    assert url == expected


@pytest.mark.parametrize('url, expected', (
    ('/repositories/john/some_project', 'repo'),
    ('/repositories/john/some_project/test', 'default'),
    ('/repositories/john/some_project/test', 'default'),
    ('/repo', 'default'),
    ('/repo/john', 'default'),
    ('/repo/john/', 'default'),
    ('/repo/john/project/', 'default'),
    ('/repo/john/project', 'default'),
))
def test_urls_views(url, expected):
    view_name = resolve(url).view_name
    assert view_name == expected

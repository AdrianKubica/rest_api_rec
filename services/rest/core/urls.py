"""
Some module comments
"""

from django.urls import path, re_path

from core.views import UserRepoView, other_endpoint

# Handle all urls with reg exp ".*" to provide predefined JSON response (Not Found 404)
urlpatterns = [
    path('repositories/<owner>/<repo_name>', UserRepoView.as_view(), name='repo'),
    re_path('.*', other_endpoint, name='default'),
]

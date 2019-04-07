"""
Some module comments
"""

from django.urls import path, re_path

from core.views import UserRepoView, DefaultView

# Handle all urls with reg exp ".*" to provide predefined JSON response (Not Found 404)
urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('repositories/<owner>/<repo_name>', UserRepoView.as_view(), name='repo'),
    # re_path('.*', DefaultView.as_view(), name='default'),
]

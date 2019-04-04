from django.urls import include, path, re_path
from core.views import DefaultView, UserRepoView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('repositories/<owner>/<repo>', UserRepoView.as_view(), name='repo'),
    re_path('.*', DefaultView.as_view(), name='default'),
]

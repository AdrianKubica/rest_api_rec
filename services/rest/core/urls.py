from django.urls import include, path
from core.views import UserRepoView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('repositories/<owner>/<repo>', UserRepoView.as_view(), name='repo'),
]

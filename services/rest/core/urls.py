from django.urls import include, path
from rest_framework import routers
from core.views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]

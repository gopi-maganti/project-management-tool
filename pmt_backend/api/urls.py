from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.restful.viewsets import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
]

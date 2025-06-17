from django.urls import path
from api.restful.viewsets.user_viewset import UserViewSet, UserLoginViewSet, GoogleLoginViewSet

urlpatterns = [
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('auth/login/', UserLoginViewSet.as_view({'post': 'login_user'}), name='user-login'),
    path('auth/google/', GoogleLoginViewSet.as_view({'post': 'google_login'}), name='google-login'),
]
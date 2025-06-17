from django.urls import path
from api.restful.viewsets.user_viewset import UserViewSet, GoogleLoginViewSet

urlpatterns = [
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('auth/login/', UserViewSet.as_view({'post': 'login_user'}), name='user-login'),
    path('auth/token/', UserViewSet.as_view({'post': 'token_login'}), name='token-login'),
    path('auth/userdata/', UserViewSet.as_view({'get': 'retrieve'}), name='user-data'),
    path('auth/google/', GoogleLoginViewSet.as_view(), name='google-login'),
]
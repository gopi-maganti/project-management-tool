from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from ..serializers.auth_serializer import LoginSerializer


class AuthViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        method='post',
        request_body=LoginSerializer,
        responses={200: openapi.Response('Login Successful', LoginSerializer)},
    )
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Google access token'),
            },
            required=['access_token'],
        ),
        responses={200: 'Returns auth token and user info'},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
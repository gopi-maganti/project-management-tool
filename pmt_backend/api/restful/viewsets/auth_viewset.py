from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from api.restful.serializers.auth_serializer import LoginTypeSerializer


class AuthViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        method='post',
        request_body=LoginTypeSerializer,
        responses={200: openapi.Response('Login successful')},
        operation_description="Login using username/password, token, or Google SSO"
    )
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginTypeSerializer(data=request.data)
        is_valid = serializer.is_valid()
        if not is_valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        login_type = data['login_type']

        if login_type == 'username_password':
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if not user:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

        elif login_type == 'token':
            token_key = data['token']
            try:
                token = Token.objects.get(key=token_key)
                return Response({"token": token.key, "user_id": token.user.id})
            except Token.DoesNotExist:
                return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        elif login_type == 'google':
            return Response({"detail": "Redirect to Google SSO endpoint"}, status=status.HTTP_200_OK)

        return Response({"detail": "Unsupported login type"}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
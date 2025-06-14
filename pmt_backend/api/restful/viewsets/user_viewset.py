from rest_framework import permissions, viewsets

from api.models import UserData
from api.restful.serializers.user_serializer import UserRegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

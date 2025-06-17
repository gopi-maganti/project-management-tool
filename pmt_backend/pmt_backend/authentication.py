from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from api.models import UserData

class CustomAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user_model = UserData
            if User.objects.filter(username=username).exists():
                user_model = User

            user = user_model.objects.get(username=username)

            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None
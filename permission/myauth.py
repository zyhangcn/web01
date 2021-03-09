from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from customer.models import User
from utility.cache import rds


class MyAuth(BaseAuthentication):
    def authenticate(self, request):
        if request.method in ["GET", "POST", "PUT", "DELETE"]:
            token = request.headers.get("token")
            user_id = rds.get(token)
            user = User.objects.get(id=user_id)
            return user, token
        else:
            return None, None

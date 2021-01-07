from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from customer.models import Token


class MyAuth(BaseAuthentication):
    def authenticate(self, request):
        if request.method in ["GET", "POST", "PUT", "DELETE"]:
            token = request.headers.get("token")
            token_ojb = Token.objects.filter(token=token).first()
            # print(token_ojb.user)
            if token_ojb:
                return token_ojb.user, token
            else:
                raise AuthenticationFailed("无效的Token")
        else:
            return None, None

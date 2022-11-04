from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import jwt
from apps.shop_app.models import UsersModel
from django.conf import settings


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_token = request.META.get("HTTP_AUTHTOKEN", "")
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        except (jwt.DecodeError, jwt.InvalidSignatureError):
            raise exceptions.AuthenticationFailed("Invalid token")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        name_nick = payload.get('name_nick')
        user = UsersModel.objects.filter(name_nick=name_nick).first()

        if not user:
            raise exceptions.AuthenticationFailed("Unauthenticated")
        return user, None

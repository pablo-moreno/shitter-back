from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import User
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.authtoken.models import Token


class UserMiddleware(BaseMiddleware):
    """
        Middleware to populate django user to the scope using the token passed in the query_string
    """
    async def resolve_scope(self, scope):
        scope["user"]._wrapped = scope.get('user')


class TokenMiddleware(UserMiddleware):
    def populate_scope(self, scope):
        qs = parse_qs(scope['query_string'].decode('utf-8'))
        token = qs.get('token')

        if not token:
            raise ValueError('Token not found')

        token = Token.objects.get(key=token)
        user = token.user

        scope['user'] = user


class JWTTokenMiddleware(UserMiddleware):
    def populate_scope(self, scope):
        qs = parse_qs(scope['query_string'].decode('utf-8'))
        token = qs.get('token')

        if not token:
            raise ValueError('Token not found')

        decoded = jwt_decode_handler(token)
        user = User.objects.get(username=decoded.get('username'))

        scope['user'] = user

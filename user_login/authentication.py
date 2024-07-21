from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
import jwt, datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.response import Response


class MobileAuthBackend:
    """
    Authenticate user using Mobile Number
    """

    def authenticate(self, request, mobile=None, accountPin=None):
        try:
            user = get_user_model().objects.get(mobile=mobile)
            if check_password(accountPin, user.accountPin):
                return user
            return None
        except (
            get_user_model().DoesNotExist,
            get_user_model().MultipleObjectsReturned,
        ):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None


class jwtTokens:
    """
    A utility class for creating JSON Web Tokens (JWTs) for authentication purposes.

    This class provides static methods to generate access and refresh tokens.
    The tokens are encoded using the HS256 algorithm and include user ID and expiration information in their payload.

    Attributes:
        None

    Methods:
        create_access_token(user_id):
            Generates an access token valid for 120 seconds with the given user ID.

        create_refresh_token(user_id):
            Generates a refresh token valid for 7 days with the given user ID.
    """

    @staticmethod
    def create_access_token(id):
        return jwt.encode(
            {
                "user_id": str(id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=120),
                "iat": datetime.datetime.utcnow(),
            },
            "access_secret",
            algorithm="HS256",
        )

    @staticmethod
    def create_refresh_token(id):
        return jwt.encode(
            {
                "user_id": str(id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
                "iat": datetime.datetime.utcnow(),
            },
            "refresh_secret",
            algorithm="HS256",
        )

    @staticmethod
    def decode_access_token(token):
        try:
            payload = jwt.decode(token, "access_secret", algorithms="HS256")
            return payload["user_id"]
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Unauthenticated {str(e)}")
    
    
    @staticmethod
    def decode_refresh_token(token):
        try:
            payload = jwt.decode(token, "refresh_secret", algorithms="HS256")
            return payload["user_id"]
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Unauthenticated {str(e)}")


class JWTAuthentication(BaseAuthentication):
    """
    Authenticates the user by getting the Bearer Token
    in the request header and then returns the user related
    to it.
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode("utf-8")
            id = jwtTokens.decode_access_token(token)

            user = get_user_model().objects.get(pk=id)
            return (user, None)

        raise exceptions.AuthenticationFailed("Unauthenticated")

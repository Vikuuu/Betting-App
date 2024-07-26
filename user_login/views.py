from rest_framework import generics, status, exceptions
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserSerializer
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .authentication import jwtTokens
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model
from .authentication import JWTAuthentication
from .models import UserToken
import datetime


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        mobile = serializer.validated_data["mobile"]
        accountPin = serializer.validated_data["accountPin"]

        try:
            user = authenticate(request, mobile=mobile, accountPin=accountPin)
            if user is None:
                raise AuthenticationFailed("Invalid Credentials")

            access_token = jwtTokens.create_access_token(user.id)
            refresh_token = jwtTokens.create_refresh_token(user.id)

            UserToken.objects.create(
                user_id=user.id,
                token=refresh_token,
                expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7),
            )

            response = Response()
            response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
            response.data = {"token": access_token}

            return response

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        except ObjectDoesNotExist:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        except MultipleObjectsReturned:
            return Response(
                {"error": "Multiple users found with this mobile number"},
                status=status.HTTP_409_CONFLICT,
            )

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Access token",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request):
        return Response(self.get_serializer(request.user).data)


class RefreshTokenView(generics.GenericAPIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "refresh_token",
                openapi.IN_HEADER,
                description="Refresh token",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: openapi.Response("Token refreshed")},
    )
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        id = jwtTokens.decode_refresh_token(refresh_token)

        if not UserToken.objects.filter(
            user_id=id,
            token=refresh_token,
            expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc),
        ).exists:
            raise exceptions.AuthenticationFailed("Unauthenticated")

        access_token = jwtTokens.create_access_token(id)

        return Response({"token": access_token})


class LogoutView(generics.GenericAPIView):

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        UserToken.objects.filter(user_id=refresh_token).delete()

        response = Response()
        response.delete_cookie(key="refresh_token")
        response.data = {"message": "success"}
        return response

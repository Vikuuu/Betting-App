from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserMobileRegistrationSerializer,
    OTPVerificationSerializer,
    PersonalDetailRegistrationSerializer,
    ActivateUserRegistrationSerializer,
)
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema


class UserMobileRegistrationView(generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserMobileRegistrationSerializer

    @swagger_auto_schema(operation_summary="Phase 1 of Registration")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "OTP sent on your number",
                "mobile": user.mobile,
                "token": user.access_medium,
            },
            status=status.HTTP_201_CREATED,
        )


class OTPVerificationView(generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = OTPVerificationSerializer

    @swagger_auto_schema(operation_summary="Phase 2 of Registration")
    def post(self, request, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_medium = token
        otp = serializer.validated_data["otp"]
        try:
            user = get_user_model().objects.get(access_medium=access_medium)
            if user.otp == otp:
                user.otp_verified = True
                user.save()
                return Response({"message": "OTP Verified"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                )
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class PersonalDetailRegistrationView(generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = PersonalDetailRegistrationSerializer

    @swagger_auto_schema(operation_summary="Phase 3 of Registration")
    def post(self, request, token):
        access_medium = token
        try:
            user = get_user_model().objects.get(access_medium=access_medium)
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Personal Details added successfully"},
            status=status.HTTP_200_OK,
        )


class ActivateUserRegistrationView(generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ActivateUserRegistrationSerializer

    @swagger_auto_schema(operation_summary="Phase 4 of Registration")
    def post(self, request, token):
        access_medium = token
        try:
            user = get_user_model().objects.get(access_medium=access_medium)
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User does not exists"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        isTermAccepted = serializer.validated_data["isTermAccepted"]
        isAgeTermAccepted = serializer.validated_data["isAgeTermAccepted"]

        if isTermAccepted == True and isAgeTermAccepted == True:
            serializer.save()
        return Response(
            {"message": "Your Account activated successfully"},
            status=status.HTTP_200_OK,
        )

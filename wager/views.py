from rest_framework import (
    generics,
    permissions,
    status,
    serializers,
)
from rest_framework.response import Response
from .serializer import (
    pick1Serializer,
    placingPick1Serializer,
    confirmingPick1Serializer,
)
from .models import pick1
from os import getenv
from user_login.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class pick1View(generics.GenericAPIView):
    serializer_class = pick1Serializer

    def get(self, request):
        pick1_record_limit = int(getenv("PICK1_RECORD_LIMIT", 15))
        pick1_data = pick1.objects.all().order_by("-draw_number")[:pick1_record_limit]
        serializer = self.get_serializer(pick1_data, many=True)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class placingPick1View(generics.GenericAPIView):
    serializer_class = placingPick1Serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "draw-id",
                openapi.IN_HEADER,
                description="Draw Id",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Please confirm the Bet."})


class confirmingPick1View(generics.GenericAPIView):
    serializer_class = confirmingPick1Serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "Draw",
                openapi.IN_HEADER,
                description="Draw id",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "pick-number",
                openapi.IN_HEADER,
                description="Pick Number",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "bet-amount",
                openapi.IN_HEADER,
                description="Bet Amount",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def post(self, request):
        data = request.data
        serializer = self.get_serializer(
            data=data,
            context={
                "user": request.user.id,
                "draw_id": request.META.get("HTTP_DRAW"),
                "pick_number": request.META.get("HTTP_PICK_NUMBER"),
                "bet_amount": request.META.get("HTTP_BET_AMOUNT"),
            },
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(
                {"message": "Bet confirmed successfully."},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

from rest_framework import generics
from .models import UserAccount
from .serializers import UserAccountSerializer


class UserAccountView(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

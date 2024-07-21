from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=10)
    accountPin = serializers.CharField(max_length=4, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["mobile", "full_name"]

from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserMobileRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["mobile"]

    def validate_mobile(self, data):
        if get_user_model().objects.filter(mobile=data).exists():
            raise serializers.ValidationError(
                "Account with this Mobile number already exists"
            )
        return data

    def create(self, validated_data):
        user_model = get_user_model()
        user = user_model.objects.create_user(**validated_data)
        user.generate_access_medium()
        user.generate_otp()
        user.save()
        # Here you would send the OTP to the user's mobile number
        # send_otp_to_mobile(user.mobile, user.otp)
        return user


class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.IntegerField()


class PersonalDetailRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["full_name", "dob", "gender", "accountPin"]
        extra_kwargs = {"accountPin": {"write_only": True}}

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.dob = validated_data.get("dob", instance.dob)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.set_password(validated_data.get("accountPin"))

        instance.save()
        return instance


class ActivateUserRegistrationSerializer(serializers.Serializer):
    isTermAccepted = serializers.BooleanField(default=False)
    isAgeTermAccepted = serializers.BooleanField(default=False)

    class Meta:
        model = get_user_model()

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.save()
        return instance

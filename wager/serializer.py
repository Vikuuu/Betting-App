from rest_framework import serializers
from .models import pick1, placingPick1


class pick1Serializer(serializers.ModelSerializer):
    class Meta:
        model = pick1
        fields = [
            "id",
            "draw_number",
            "draw_name",
            "draw_time",
            "draw_date_time",
            "game_date_time",
        ]


class placingPick1Serializer(serializers.ModelSerializer):
    class Meta:
        model = placingPick1
        fields = ["user", "draw_number", "pick_number", "bet_amount"]
        extra_kwargs = {
            "user": {"write_only": True},
            "draw_number": {"write_only": True},
        }

    def create(self, validated_data):
        bet_amount = validated_data.pop("bet_amount", 0) * 100

        pick1_bet = placingPick1.objects.create(
            **validated_data,
            bet_amount=bet_amount,
        )
        return pick1_bet


class confirmingPick1Serializer(serializers.ModelSerializer):
    class Meta:
        model = placingPick1
        fields = ["is_confirmed"]

    def create(self, validated_data):
        user = self.context["user"]
        draw_number = self.context["draw_number"]
        try:
            pick = placingPick1.objects.get(user=user, draw_number=draw_number)
            pick.is_confirmed = True
            pick.save()
            return pick
        except placingPick1.DoesNotExist:
            raise serializers.ValidationError(
                "Pick record not found for the user and draw_number."
            )

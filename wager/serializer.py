from rest_framework import serializers
from .models import pick1, CustomerWager
from .validators import pick_validation
from django.contrib.auth import get_user_model


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


class placingPick1Serializer(serializers.Serializer):
    pick_number = serializers.IntegerField(validators=[pick_validation])
    bet_amount = serializers.IntegerField()


class confirmingPick1Serializer(serializers.ModelSerializer):
    is_confirmed = serializers.BooleanField(default=False)

    class Meta:
        model = CustomerWager
        fields = [
            "is_confirmed",
        ]

    def create(self, validated_data):
        is_confirmed = validated_data.pop("is_confirmed", None)
        user_id = self.context.get("user")
        user = get_user_model().objects.get(id=user_id)
        draw_id = self.context.get("draw_id")
        draw = pick1.objects.get(id=draw_id)
        pick_number = self.context.get("pick_number")
        bet_amount = self.context.get("bet_amount")
        if is_confirmed:
            pick = CustomerWager.objects.create(
                user=user,
                draw_id=draw,
                pick_number=pick_number,
                bet_amount=bet_amount,
                pick_name=CustomerWager.Pick.PICK_1,
            )
            pick.save()
            return pick

from rest_framework import serializers
from .models import pick1


class pick1Serializer(serializers.ModelSerializer):
    class Meta:
        model = pick1
        fields = [
            "draw_number",
            "draw_name",
            "draw_time",
            "draw_date_time",
            "game_date_time",
        ]

from django.db import models
import uuid
from django.conf import settings
from .validators import pick_validation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model


class pick1(models.Model):
    class drawNameChoice(models.TextChoices):
        MORNING = "M", "Morning"
        AFTERNOON = "A", "Afternoon"
        EVENING = "E", "Evening"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    draw_number = models.IntegerField(unique=True)
    draw_name = models.CharField(max_length=1, choices=drawNameChoice)
    draw_date = models.DateField(auto_now_add=True)
    draw_time = models.TimeField(auto_now_add=True)
    draw_date_time = models.DateTimeField(auto_now_add=True)
    game_date_time = models.DateTimeField()
    is_draw_posted = models.BooleanField(default=False)
    is_draw_approved = models.BooleanField(default=False)
    is_draw_executed = models.BooleanField(default=False)
    is_draw_execution_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["draw_number"]),
        ]

    def __str__(self) -> str:
        return f"Draw Number: {self.draw_number}"


class placingPick1(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="placingPick1",
        # to_field="mobile",
    )
    draw_number = models.ForeignKey(
        pick1, on_delete=models.CASCADE, related_name="placingpick1"
    )
    pick_number = models.SmallIntegerField(validators=[pick_validation])
    is_confirmed = models.BooleanField(default=False)
    bet_amount = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "draw_number")

    # @staticmethod
    # def get_user_by_mobile(mobile):
    #     try:
    #         return get_user_model().objects.get(mobile=mobile)
    #     except ObjectDoesNotExist:
    #         return None

    def __str__(self):
        return f"{self.user.full_name} - Draw: {self.draw_number} - Pick: {self.pick_number}"

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


class CustomerWager(models.Model):
    class Pick(models.TextChoices):
        PICK_1 = "P1", "Pick 1"
        PICK_4 = "P4", "Pick 4"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_wager",
    )
    draw_id = models.ForeignKey(
        pick1,
        on_delete=models.CASCADE,
        related_name="customer_wagers",
    )
    pick_name = models.CharField(max_length=2, choices=Pick.choices)
    pick_number = models.SmallIntegerField(validators=[pick_validation])
    bet_amount = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "draw_id")

    def __str__(self):
        return f"{self.user.full_name} - Draw: {self.draw_number} - Pick: {self.pick_number}"

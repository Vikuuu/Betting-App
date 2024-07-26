from django.db import models
import uuid


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

from django.db import models
import uuid


class UserToken(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

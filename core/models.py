from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from django.contrib.auth.hashers import make_password, check_password
from .validators import validate_phone_number
from .helpers import generate_access_medium, generate_otp
from .managers import UserManager
from django.conf import settings
from wager.models import CustomerWager


class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    access_medium = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(
        max_length=10, unique=True, validators=[validate_phone_number]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(null=True, blank=True)
    otp_verified = models.BooleanField(default=False)
    full_name = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.MALE)
    idNumber = models.CharField(max_length=50)
    accountPin = models.CharField(max_length=4, blank=True)
    password = None

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(fields=["mobile"]),
        ]

    def __str__(self) -> str:
        return self.full_name

    def generate_access_medium(self):
        self.access_medium = generate_access_medium()
        self.save()

    def generate_otp(self):
        self.otp = generate_otp()
        self.save()

    def set_password(self, raw_password):
        self.accountPin = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        return check_password(raw_password, self.accountPin)


class Transactions(models.Model):
    class TransactionType(models.TextChoices):
        BET = "bet", "Bet"
        DEPOSIT = "deposit", "Deposit"
        PAYOUT = "payout", "Payout"
        WITHDRAWAL = "withdrawal", "Withdrawal"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
    )
    type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    bet_id = models.ForeignKey(
        CustomerWager,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.user.username} - Type: {type}"

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid, random, secrets
from django.contrib.auth.hashers import make_password
from .validators import validate_phone_number


class UserManager(BaseUserManager):

    def create_user(self, mobile, accountPin=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not mobile:
            raise ValueError("Users must have an Mobile number")

        user = self.model(mobile=mobile, **extra_fields)

        if accountPin:
            user.set_password(accountPin)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, accountPin=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            mobile=mobile,
            accountPin=accountPin,
            **extra_fields,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
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
        self.access_medium = secrets.token_urlsafe(16)
        self.save()

    def generate_otp(self):
        self.otp = random.randint(100000, 999999)
        self.save()

    def set_password(self, raw_password):
        self.accountPin = make_password(raw_password)
        self._password = raw_password

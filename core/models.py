from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid, random


class UserManager(BaseUserManager):

    def create_user(self, mobile, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not mobile:
            raise ValueError("Users must have an Mobile number")

        user = self.model(mobile=mobile, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            mobile=mobile,
            password=password,
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
    mobile = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField()
    full_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.MALE)
    idNumber = models.CharField(max_length=50)
    password = models.CharField(max_length=4, db_column="accountPin")

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

    def generate_otp(self):
        self.otp = random.randint(100000, 999999)
        self.save()

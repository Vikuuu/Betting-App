from django.contrib.auth.models import BaseUserManager


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
        if accountPin is None:
            accountPin = "0000"

        user = self.create_user(
            mobile=mobile,
            accountPin=accountPin,
            **extra_fields,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

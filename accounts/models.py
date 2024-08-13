from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from accounts.abstracts import AbstractProfileModel, TimeStampedModel, UniversalIdModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_verified", True)

        if not password:
            raise ValueError("Password is required")
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if kwargs.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if kwargs.get("is_verified") is not True:
            raise ValueError("Superuser must have is_verified=True.")

        return self._create_user(email, password, **kwargs)


class User(
    AbstractBaseUser,
    PermissionsMixin,
    UniversalIdModel,
    TimeStampedModel,
    AbstractProfileModel,
):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_personal = models.BooleanField(default=False)
    is_ceo = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    objects = UserManager()
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

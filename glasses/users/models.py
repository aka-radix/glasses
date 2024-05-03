from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from glasses.products.models import Currency

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    currency = models.CharField(
        choices=Currency.choices,
        max_length=3,
        default="USD",
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

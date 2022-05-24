from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


class Accounts(AbstractUser):
    user_uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True)
    username = models.CharField(max_length=150, null=True)
    account_balance = models.FloatField(default=0)
    # password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []

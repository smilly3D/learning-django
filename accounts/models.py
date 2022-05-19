from uuid import uuid4
from django.db import models


class Accounts(models.Model):
    user_uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True)
    account_balance = models.FloatField(default=0)
    password = models.CharField(max_length=255)

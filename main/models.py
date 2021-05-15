import logging
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models

from main.api import get_client

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Exchanges(models.TextChoices):
    BINANCE = "binance"
    BYBIT = "bybit"
    # List goes on


class Account(models.Model):
    """
    API credentials of user's account
    """


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    api_keys = models.CharField(max_length=250)
    secret_key = models.CharField(max_length=250)


    def get_account_client(self):
        return get_client(
            exchange_id=self.exchange, api_key=self.api_key, secret=self.secret
        )


class Currency(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    short_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.pk}: {self.short_code}"


class Input(models.Model):
    api_key = models.CharField(max_length=250)
    secret = models.CharField(max_length=250)
    api_key = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='api_key')
    secret = models.ForeignKey(Account, on_delete= models.CASCADE,related_name='secret')



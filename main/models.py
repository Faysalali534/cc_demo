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

    exchange = models.CharField(max_length=250, choices=Exchanges.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=250)
    secret = models.CharField(max_length=250)
    password = models.CharField(max_length=250, blank=True, null=True)
    default_fee_rate = models.DecimalField(
        max_digits=30, decimal_places=4, default=Decimal(0.1)
    )

    def get_account_client(self):
        return get_client(
            exchange_id=self.exchange, api_key=self.api_key, secret=self.secret
        )


class Currency(models.Model):

    name = models.CharField(max_length=50, blank=True, null=True)
    short_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.pk}: {self.short_code}"

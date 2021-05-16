import logging

import django
from django.contrib.auth.models import User
from django.db import models

from main.api import get_client

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Exchanges(models.TextChoices):
    BINANCE = "binance"
    BYBIT = "bybit"
    # List goes on


class AccountManager(models.Manager):

    def lookup(self, email):
        """
        this methods looks for requested email

        Args:
            email (str): requested email to look in account table

        Returns:
            [Query Set]: it returns the row of table with requested email
        """
        return self.filter(user__email=email)

    def no_verified(self):
        """
        Returns accounts that have not been verified

        Returns:
            [Query Set]: it returns the rows which have is_active as false
        """
        return self.filter(is_active=False)

    def create_account(self, user_data, api_key, secret_key):
        """
        it creates account with requested user and middle_name

        Args:
            user_data ([type:user model django]): builtin django user model
            api_key ([type:str]): account with middle name

        Returns:
            [type:account instance]: account instance which was created
        """
        user_password = user_data.pop('password')
        user_data['username'] = user_data.get('email')
        user = User(**user_data)
        user.set_password(raw_password=user_password)
        user.save()
        account = Account(user=user, api_key=api_key, secret_key=secret_key)
        account.save()
        return account


class Account(models.Model):
    """
    API credentials of user's account
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.TextField(unique=True)
    secret_key = models.TextField(unique=True)
    objects = AccountManager()

    def get_account_client(self):
        return get_client(
            api_key=self.api_key, secret=self.secret
        )


class Currency(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    short_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.pk}: {self.short_code}"


class Input(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    Currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(default=django.utils.timezone.now)
    category = models.CharField(max_length=30, default='inverse')

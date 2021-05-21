import logging

import django
from django.contrib.auth.models import User
from django.db import models

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

    def __str__(self):
        return f"<id:{self.pk}> - <user:{self.user.username}>"


class Currency(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Exchange(models.Model):
    name = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Input(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(default=django.utils.timezone.now)
    category = models.CharField(max_length=30, default='inverse')

    def __str__(self):
        return f"<id:{self.pk}> - <currency:{self.currency.name}> - <user:{self.account.user.username}> - <account_id:{self.account.id}>"


class Log(models.Model):
    input_id = models.IntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField(default=django.utils.timezone.now)
    end_date = models.DateTimeField(default=django.utils.timezone.now)
    category = models.CharField(max_length=30, default='inverse')
    info = models.TextField(default='')
    status = models.CharField(max_length=30, default='successful')


class RecordedData(models.Model):
    Input = models.ForeignKey(Input, on_delete=models.CASCADE)
    before = models.CharField(max_length=60)
    amount = models.CharField(max_length=60)
    after = models.CharField(max_length=60)
    ledger_id = models.CharField(max_length=60)
    realised_pnl = models.CharField(max_length=60)
    captured_date = models.DateTimeField()
    roi = models.CharField(max_length=60)
    type = models.CharField(max_length=30, default='')

    def __str__(self):
        return f"<ledger_id:{self.ledger_id}> - <realised_pnl:{self.realised_pnl}> - <type:{self.type}> - <input_id:{self.Input.id}>"

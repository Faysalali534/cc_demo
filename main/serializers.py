from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import Currency
from main.models import Account
from main.models import Input
from main.models import RecordedData
from main.models import Exchange
from main.models import Log


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}


class AccountSerializer(serializers.ModelSerializer):
    # nested serializer
    user = UserSerializer()

    class Meta:
        model = Account
        fields = ['id', 'api_key', 'secret_key', 'user']

    def create(self, validated_data):
        account_info = validated_data.pop("user")
        account = Account.objects.create_account(
            user_data=account_info, api_key=validated_data.get("api_key"), secret_key=validated_data.get("secret_key")
        )
        return account


class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class RecordedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordedData
        fields = '__all__'


class ReteriveInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = '__all__'
        depth = 1


class AccountRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'api_key', 'secret_key']


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
        depth = 1

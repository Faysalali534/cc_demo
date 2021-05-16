from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import Account


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
        fields = ['api_key', 'secret_key', 'user']

    def create(self, validated_data):
        account_info = validated_data.pop("user")
        account = Account.objects.create_account(
            user_data=account_info, api_key=validated_data.get("api_key"), secret_key=validated_data.get("secret_key")
        )
        return account

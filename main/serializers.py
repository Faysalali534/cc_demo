from rest_framework import serializers

from main.models import Account


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [ 'user', 'api_key', 'secret']

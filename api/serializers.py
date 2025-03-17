from rest_framework import serializers
from .models import User, Account, Destination, AccountMember, Log

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'created_at')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'website', 'app_secret_token', 'created_at')
        read_only_fields = ('app_secret_token',)

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('id', 'account', 'url', 'http_method', 'headers')

class AccountMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountMember
        fields = ('id', 'account', 'user', 'role')

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = (
            'event_id', 'account', 'destination', 'status',
            'received_timestamp', 'processed_timestamp', 'received_data'
        ) 
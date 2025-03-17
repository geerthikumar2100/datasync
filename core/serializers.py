from rest_framework import serializers
from core.models import Account, Destination, Log, User, AccountMember, Role

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        return user

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

class AccountMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountMember
        fields = "__all__"

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = "__all__"

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = "__all__"

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

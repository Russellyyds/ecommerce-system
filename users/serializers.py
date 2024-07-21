from rest_framework import serializers
from .models import User, Address


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = User
        # fields = "__all__"
        fields = ["id", "username", "email", "mobile", "avatar", "last_name"]


class AddrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

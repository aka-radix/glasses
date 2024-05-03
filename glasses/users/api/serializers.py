from django.contrib.auth import password_validation
from rest_framework import serializers

from glasses.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("id",)

    def validate_password(self, password) -> None:
        """Run password validation."""

        password_validation.validate_password(password=password)
        return password

    def create(self, validated_data) -> User:
        """Register user via the manager."""

        return User.objects.create_user(  # type: ignore
            email=validated_data["email"],
            password=validated_data["password"],
        )


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["currency"]

    def update(self, instance, validated_data):
        instance.currency = validated_data.get("currency", instance.currency)
        instance.save()
        return instance

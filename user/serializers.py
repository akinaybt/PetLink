from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    This class is a serializer for the CustomUser model.

    It is used to convert the CustomUser model instances into JSON data and
    vice versa. It ensures that the password is hashed before saving into the
    database and validates the password complexity using Django's built-in
    validators.    """
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
        )
        extra_kwargs = {
            'password': {'write_only': True}  # Don't show the password in the API response
        }

    def validate_password(self, value):
        try:
            validate_password(value)  # Validation using Django's built-in methods.
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data['password'] = make_password(password)
        instance = super().create(validated_data)
        return instance

class LoginSerializer(serializers.Serializer):
    """
    Handles serialization for user login data.

    This class is designed for validating and processing user login information,
    ensuring that all required fields are provided and properly formatted.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

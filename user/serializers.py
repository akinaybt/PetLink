from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели CustomUser. Включает проверку сложности пароля.
    """
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
            'password': {'write_only': True}  # Не показывать пароль в ответе API
        }

    def validate_password(self, value):
        """
        Проверка сложности пароля.
        """
        try:
            validate_password(value)  # Проверка с использованием встроенных методов Django.
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        """
        Хэширование пароля перед сохранением.
        """
        password = validated_data.pop('password', None)
        validated_data['password'] = make_password(password)  # Хэширование пароля
        instance = super().create(validated_data)  # Создание объекта пользователя
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # Только email
    password = serializers.CharField(write_only=True, required=True)  # Только пароль

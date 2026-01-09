from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    """
    Serializer for the user profile, showing a safe subset of user data.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'email']
#
# class CustomUserSerializer(serializers.ModelSerializer):
#     """
#     CustomUserSerializer сериалайзер для модели CustomUser.
#     Нужен для преобразования данных модели CustomUser в формат JSON.
#     """
#     class Meta:
#         model = CustomUser
#         fields = (
#             'id',
#             'first_name',
#             'last_name',
#             'username',
#             'password',
#             'email',
#         )
#
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data.get('password'))
#         return super(CustomUserSerializer, self).create(validated_data)

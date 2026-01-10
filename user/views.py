from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomUserSerializer, LoginSerializer
from .models import CustomUser


class CustomUserRegistrationView(GenericAPIView):
    """
    Представление для регистрации нового пользователя.
    Ограничено только действиями для регистрации.
    """
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    """
    GenericAPIView для аутентификации пользователя.
    Возвращает токен после успешного логина.
    """
    serializer_class = LoginSerializer  # Используйте сериалайзер, если хотите валидировать входящие данные.
    # permission_classes = AllowAny

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            # Аутентифицируем пользователя, чтобы связать данные с сессией
            login(request, user)  # Это добавляет пользователя в текущую сессию

            # Генерация токена
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key,
                    "user_id": user.id,
                    "email": user.email,
                    "first_name": user.first_name
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
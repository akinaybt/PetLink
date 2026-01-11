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
    Handles user registration with custom logic.

    This class provides an API endpoint for registering new users. It processes
    incoming POST requests, validates the data using a serializer, and creates
    a new user upon successful validation. If the data validation fails, it
    returns the appropriate error messages.
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
    Handles user login through REST API.

    This class-based view provides functionality for authenticating users via
    email and password. Upon successful authentication, it attaches the user
    to the current session and generates or retrieves an authentication token
    for the user. The view is serializer-driven, allowing input data to be validated
    through the specified serializer.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            # Authenticating the user to link the data to the session
            login(request, user)  # Adds the user to the current session
            # Token generation
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
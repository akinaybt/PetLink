from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import *
from .models import CustomUser


# Create your views here.
class CustomUserViewSet(viewsets.ModelViewSet):
    """Представление CustomUserViewSet написано для модели CustomUser. """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
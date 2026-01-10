from django.urls import path
# from .views import CustomUserRegistrationView, LoginView
from .views import *

urlpatterns = [
    path('register/', CustomUserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='user-login'),
]
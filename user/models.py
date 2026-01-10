from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Менеджер для модели CustomUser, позволяющий создавать пользователей
    и суперпользователей с уникальным email.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Метод для создания суперпользователей.
        Использует email вместо username.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя. Вместо username используется email.
    """
    username = None  # Убираем поле username
    email = models.EmailField(unique=True, blank=False)  # Делаем email уникальным

    USERNAME_FIELD = 'email'  # Используем email в качестве уникального идентификатора
    REQUIRED_FIELDS = []  # Поля, обязательные для заполнения при создании суперпользователя

    objects = CustomUserManager()

    def __str__(self):
        return self.email
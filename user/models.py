from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    CustomUserManager is used to manage the creation of user and superuser
    objects with email addresses instead of usernames.

    This class provides two methods: `create_user` for creating regular users
    and `create_superuser` specifically for creating superusers with additional
    privileges. It ensures required fields are set and handles password management.

    :ivar model: The user model that this manager interacts with. This is typically
        the model specified in the `AUTH_USER_MODEL` setting.
    :type model: Any
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        A method for creating superusers.
        Uses email instead of username.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser should have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser should have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    A custom user model for authentication.

    The `CustomUser` class provides an extension of the default Django `AbstractUser` model
    by removing the username field and using the email field as the unique identifier for authentication.
    This model is suitable for applications where email-based login is required.

    :ivar email: The email address of the user. Must be unique and cannot be blank.
    :type email: EmailField
    :ivar USERNAME_FIELD: Specifies the field used as the unique identifier for authentication, set to 'email'.
    :type USERNAME_FIELD: str
    :ivar REQUIRED_FIELDS: Specifies the fields required when creating a superuser, set to an empty list.
    :type REQUIRED_FIELDS: list
    """
    username = None  # Убираем поле username
    email = models.EmailField(unique=True, blank=False)  # Email must be unique

    USERNAME_FIELD = 'email'  # Email is used as unique identifier
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
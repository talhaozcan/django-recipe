from django.db import models
from django.contrib.auth.models import (

    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves new user via email"""

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Please provide a valid email address.")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """creates and saves new superuser via email"""

        user = self.create_user(email, password)
        user.is_stuff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model to use just email"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_stuff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

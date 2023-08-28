from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from core.abstract.models import AbstractModel, AbstractManager


class UserManager(BaseUserManager, AbstractManager):
    def create_user(self, email, password=None, **kwargs):
        """Create and return a `User` with an email and password."""
        if email is None:
            raise TypeError("Users must have an email")
        if password is None:
            raise TypeError('Users must have a password')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions
        """
        if password is None:
            raise TypeError("Superusers must have a password")
        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True  # Fixed the attribute name
        user.save(using=self._db)
        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # bio = models.TextField(null=True)
    # avatar = models.ImageField

    USERNAME_FIELD = 'email'
    # EMAIL_FIELD = "email"
    # No additional fields required for registration
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
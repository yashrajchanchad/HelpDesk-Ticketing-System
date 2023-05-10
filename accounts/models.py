from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

import logging


logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    is_it_manager = models.BooleanField('IT Manager', default=False)
    is_it_engineer = models.BooleanField('IT Engineer', default=False)
    phone_number = models.PositiveIntegerField('phone', null=True)
    job_title = models.CharField('title', max_length=100 , null=True)
    username = None
    USERNAME_FIELD = 'email'
    department = models.CharField('department', max_length=100, null=True)
    city = models.CharField('city', max_length=100, null=True)
    REQUIRED_FIELDS = []
    objects = UserManager()

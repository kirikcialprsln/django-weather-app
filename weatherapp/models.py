from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'User Name',
        max_length=30,
        unique=True,
        validators=[username_validator]

    )
    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(
        default=True
    )
    user_permission = models.CharField(
        max_length=20,
        default='user'

    )
    last_login = models.DateTimeField(
        null=True,
        blank=True

    )
    date_joined = models.DateTimeField(
        auto_now_add=True

    )
    is_staff = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=False
    )
    is_admin = models.BooleanField(
        default=False
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ( {self.username} )"
        return self.username


class Meta:
    verbose_name = 'User'
    verbose_name_plural = 'User'
    db_table = 'User'
    ordering = ['created']


class Log(models.Model):
    ip = models.GenericIPAddressField()
    current_time = models.DateTimeField()
    current_user = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    time = models.CharField(max_length=20, unique=False, null=True)

    class Meta:
        verbose_name_plural = 'information'


class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime, timedelta

# Create your models here.


class StudentGenre(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Major(models.Model):
    code = models.CharField(max_length=10, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return "[{code}] {name}".format(code=self.code, name=self.name)


class Profession(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password, genre, profession, cui, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The username must be set'))
        if not email:
            raise ValueError(_('The Email must be set'))
        if not cui:
            raise ValueError(_('The cui must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, genre=StudentGenre(pk=genre), profession=Profession(pk=profession), cui=cui, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, genre, profession, cui, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, username, password, genre, profession, cui, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    genre = models.ForeignKey(
        StudentGenre,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1,
    )
    profession = models.ForeignKey(
        Profession,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1,
    )
    activated = models.BooleanField(
        null=False,
        default=False
    )
    cui = models.CharField(
        max_length=13,
        unique=True,
        null=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'genre', 'profession', 'cui']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ValidationToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    code = models.CharField(max_length=50, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{user} code:{code}".format(user=self.user, code=self.code)

    def is_valid(self):
        delta = now() - self.created_at

        return delta.seconds <= 60*10

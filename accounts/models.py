from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class TokenQuerySet(models.QuerySet):
    pass

class TokenManager(models.Manager):
    def get_queryset(self):
        return TokenQuerySet(self.model, using=self._db)

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a user with the given email address and password
        """
        if not email:
            raise ValueError("Email is necessary to create a user")
        email      = self.normalize_email(email)
        user       = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Creates a superuser with email address and password
        """
        if not email:
            raise ValueError("Email is necessary to create a user")

        user = self.model(email=email, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    email           = models.EmailField(('email address'), unique=True)
    phone_number    = models.CharField(('phone number'), max_length=14, blank=True)
    house_add       = models.TextField(('house address'), blank=True)
    off_add         = models.TextField(('Office address'), blank=True)

    USERNAME_FIELD          = 'email'
    REQUIRED_FIELDS         = []

    objects = CustomUserManager()


class Token_keeper(models.Model):
    User            = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token    = models.CharField(max_length=200)
    refresh_token   = models.CharField(max_length=200)
    allowed         = models.BooleanField(default=True)

    objects = TokenManager

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

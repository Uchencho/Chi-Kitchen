from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

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

# Create your models here.
# class User(AbstractUser):
#     email           = models.EmailField(_('email address'), unique=True)
#     first_name      = models.CharField(_('first name'), max_length=30, blank=True)
#     last_name       = models.CharField(_('last name'), max_length=30, blank=True)
#     phone_number    = models.CharField(_('phone number'), max_length=14, blank=True)
#     house_add       = models.TextField(_('house address'), blank=True)
#     off_add         = models.TextField(_('Office address'), blank=True)
#     last_login      = models.DateTimeField(_('last login'), auto_now_add=True, auto_now=True)
#     date_joined     = models.DateTimeField(_('date joined'), auto_now_add=True)
#     is_active       = models.BooleanField(_('active'), default=True)
#     is_staff        = models.BooleanField(_('staff'), default=False)
#     is_superuser    = models.BooleanField(_('superuser'), default=False)

#     USERNAME_FIELD          = 'email'
#     REQUIRED_FIELDS         = []
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UsersManager
from django.utils.timezone import now, timedelta


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UsersManager()

    def __str__(self):
        return self.email
    

    def generate_otp(self):
        import random
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.otp_expiry = now() + timedelta(minutes=10)  # OTP expires in 10 minutes
        self.save()
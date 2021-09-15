from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.dispatch import receiver
# from django.urls import reverse
# from django_rest_passwordreset.signals import reset_password_token_created
# from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

GENDER_CHOICE = [
    (1, "Nam"),
    (2, "Nữ"),
    (0, "Khác")
]


class MyUsers(AbstractUser):
    email = models.EmailField(_('email address'), max_length=200, unique=True)
    phone = models.CharField(_('phone'), max_length=15, blank=True, null=True)
    gender = models.IntegerField(_('gender'), choices=GENDER_CHOICE, default=1, blank=True, null=True)
    address = models.CharField(_('address'), max_length=100, blank=True, null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    avatar = models.FileField(_('avatar'), upload_to='image/avatar', blank=True, null=True, default="avatar.jpg")
    time_create = models.DateTimeField(_('time create'), auto_now_add=True)
    time_update = models.DateTimeField(_('time update'), auto_now=True)


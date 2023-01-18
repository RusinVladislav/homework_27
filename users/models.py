from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from users.validators import check_birth_date, check_email_address


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return self.name


class UserRoles(models.TextChoices):
    MEMBER = "member", _("member")
    MODERATOR = "moderator", _("moderator")
    ADMIN = "admin", _("admin")


class User(AbstractUser):
    role = models.CharField(max_length=9, choices=UserRoles.choices)
    age = models.PositiveSmallIntegerField()
    locations = models.ManyToManyField(Location)
    birth_date = models.DateField(verbose_name="Дата рождения", validators=[check_birth_date], blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True, validators=[check_email_address])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

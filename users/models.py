from django.db import models
from django.contrib.auth.models import AbstractUser
from common.db import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel, models.Model):
    """user model"""
    mobile = models.CharField(max_length=11, verbose_name="phone number")
    avatar = models.ImageField(verbose_name="user avatar", blank=True, null=True)

    def set_password(self, raw_password):
        super().set_password(raw_password)

    def check_password(self, raw_password):
        return super().check_password(raw_password)

    class Meta:
        db_table = 'users'
        verbose_name = "User Table"


class Address(models.Model):
    """address model"""
    user = models.ForeignKey('User', verbose_name="belong user", on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, verbose_name="User Phone Number", default="")
    name = models.CharField(max_length=20, verbose_name="User Name")
    province = models.CharField(max_length=20, verbose_name="Province")
    city = models.CharField(max_length=20, verbose_name="City")
    county = models.CharField(max_length=20, verbose_name="County", default="")
    address = models.CharField(max_length=200, verbose_name="Address", default="")  # more details
    is_default = models.BooleanField(verbose_name="Default Address", default=False)

    class Meta:
        db_table = "address"
        verbose_name = "Delivery Address Table"


class Area(models.Model):
    """Country:0 Province:1  City:2 County:3   model """
    pid = models.IntegerField(verbose_name="parent id", default=0)
    name = models.CharField(verbose_name="parent name", max_length=20)
    level = models.CharField(verbose_name="level", max_length=20)

    class Meta:
        db_table = "area"
        verbose_name = "Area Table"


class VerifCode(models.Model):
    """VerifCode"""
    mobile = models.CharField(verbose_name="phone number", max_length=11)
    code = models.CharField(verbose_name="verif code", max_length=6)
    create_time = models.DateTimeField(verbose_name="create time", auto_now_add=True)

    class Meta:
        db_table = "verif_code"
        verbose_name = "Phone Verif Code Table"

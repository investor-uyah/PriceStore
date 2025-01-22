from django.db import models
from django.contrib.auth.models import User
import datetime

class Memebers(models.Model):
    shopname = models.CharField(max_length=100, null=True, blank=True, verbose_name='shopname')
    ownersname = models.CharField(max_length=100, null=True, blank=True, verbose_name='ownersname')
    phone = models.CharField(max_length=14, null=True, blank=True, verbose_name='phone')
    # Use a datetime.date object for default value
    joined_date = models.DateField(auto_now_add=True, verbose_name='joined_date')
    bio = models.CharField(max_length=100, null=True, blank=True, verbose_name='bio')

class Price(models.Model):
    foodstuff = models.CharField(max_length=100, blank=False, verbose_name='foodstuff')
    price = models.IntegerField(null=True, blank=True, verbose_name='price')  # Use blank=True for optional price
    description = models.CharField(max_length=100, blank=True, verbose_name='description')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

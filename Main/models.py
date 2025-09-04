from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import F
from .choices import STATES_CHOICES, FOODSTUFFS_CHOICES
import datetime

class Memebers(models.Model):
    shopname = models.CharField(max_length=100, null=True, blank=True, verbose_name='shopname')
    ownersname = models.CharField(max_length=100, null=True, blank=True, verbose_name='ownersname')
    phone = models.CharField(max_length=14, null=True, blank=True, verbose_name='phone')
    # Use a datetime.date object for default value
    joined_date = models.DateField(auto_now_add=True, verbose_name='joined_date')
    bio = models.CharField(max_length=100, null=True, blank=True, verbose_name='bio')

class Price(models.Model):
    foodstuff = models.CharField(max_length=100, choices=FOODSTUFFS_CHOICES, verbose_name='foodstuff')
    price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(100)], verbose_name='price') 
    description = models.CharField(max_length=100, blank=True, verbose_name='description')
    market_store_name = models.CharField(max_length=100, blank=True, verbose_name='market or store name')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')

   
    state = models.CharField(max_length=50, choices=STATES_CHOICES, verbose_name='state')
    lga = models.CharField(max_length=100, blank=True, verbose_name='local government area')

    def __str__(self):
        return self.foodstuff

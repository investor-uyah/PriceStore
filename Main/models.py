from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
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
    foodstuff = models.CharField(max_length=100, choices=FOODSTUFFS_CHOICES, verbose_name='foodstuff', blank=False)
    price = models.IntegerField(validators=[MinValueValidator(100)], verbose_name='price', null=False, blank=False)
    description = models.CharField(max_length=100, blank=False, verbose_name='description')
    market_store_name = models.CharField(max_length=100, blank=False, verbose_name='market or store name')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    
    
    state = models.CharField(max_length=50, choices=STATES_CHOICES, verbose_name='state', blank=False)
    lga = models.CharField(max_length=100, blank=False, verbose_name='local government area')

    def __str__(self):
        return self.foodstuff

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set", # Add this line
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions_set", # Add this line
        related_query_name="custom_user_permission",
    )
    # Your other fields like phone_number
    phone_number = models.CharField(max_length=15, blank=False, null=False)
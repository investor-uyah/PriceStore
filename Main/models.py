from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator
from django.conf import settings
from .choices import STATES_CHOICES, FOODSTUFFS_CHOICES
import datetime

class Members(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships', verbose_name='Associated User')
    shopname = models.CharField(max_length=100, null=False, blank=False, verbose_name='Shop Name')
    ownersname = models.CharField(max_length=100, null=False, blank=False, verbose_name='Owner\'s Name')
    phone = models.CharField(max_length=14, null=False, blank=False, verbose_name='Phone Number')
    company_email = models.EmailField(max_length=254, null=True, blank=True, verbose_name='Company Email')
    state = models.CharField(max_length=50, choices=STATES_CHOICES, verbose_name='state', blank=False)
    lga = models.CharField(max_length=100, blank=False, verbose_name='local government area')
    address = models.CharField(max_length=100, blank=False, verbose_name='address')
    joined_date = models.DateTimeField(auto_now_add=True, verbose_name='Joined Date')
    bio = models.CharField(max_length=100, null=False, blank=False, verbose_name='Bio')
    
    def __str__(self):
        return f"{self.shopname} ({self.ownersname})"

class Price(models.Model):
    foodstuff = models.CharField(max_length=100, choices=FOODSTUFFS_CHOICES, verbose_name='foodstuff', blank=False)
    price = models.IntegerField(validators=[MinValueValidator(100)], verbose_name='price', null=False, blank=False)
    description = models.CharField(max_length=100, blank=False, verbose_name='description')
    market_store_name = models.CharField(max_length=100, blank=False, verbose_name='market or store name')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='author')
    
    
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
        related_name="main_app_user_groups",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="main_app_user_permissions",
        related_query_name="custom_user_permission",
    )
    phone_number = models.CharField(max_length=15, blank=False, null=False)
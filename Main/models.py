from django.db import models

# Create your models here.

class Memebers(models.Model):
    shopname = models.CharField(max_length=255, null=True, verbose_name=('shopname'))
    ownersname = models.CharField(max_length=255, null=True, verbose_name=('ownersname'))
    phone = models.IntegerField(null=True, verbose_name='phone')
    joined_date = models.DateField(null=True, verbose_name='joined_date')
    bio = models.CharField(max_length=255, null=True, verbose_name='bio')
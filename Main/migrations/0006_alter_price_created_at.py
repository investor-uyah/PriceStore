# Generated by Django 5.1.3 on 2025-01-23 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_price_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
        ),
    ]

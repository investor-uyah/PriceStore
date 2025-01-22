# Generated by Django 5.1.3 on 2025-01-10 23:15

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_memebers_bio'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='memebers',
            name='bio',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='bio'),
        ),
        migrations.AlterField(
            model_name='memebers',
            name='joined_date',
            field=models.DateField(auto_now_add=True, default=datetime.date(2025, 1, 1), verbose_name='joined_date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='memebers',
            name='ownersname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ownersname'),
        ),
        migrations.AlterField(
            model_name='memebers',
            name='phone',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='memebers',
            name='shopname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='shopname'),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foodstuff', models.CharField(max_length=100, verbose_name='foodstuff')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='price')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='description')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

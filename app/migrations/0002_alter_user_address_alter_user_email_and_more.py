# Generated by Django 5.0.4 on 2024-04-08 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='User',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='User',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='User',
            name='phoneNumber',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]

# Generated by Django 5.0.4 on 2024-05-05 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_emailverification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='verification_code',
        ),
    ]

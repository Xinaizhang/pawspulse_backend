# Generated by Django 5.0.4 on 2024-04-24 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='User',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='User',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='User',
            new_name='user',
        ),
    ]
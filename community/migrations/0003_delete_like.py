# Generated by Django 5.0.4 on 2024-04-25 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_rename_user_comment_user_rename_user_like_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='like',
        ),
    ]
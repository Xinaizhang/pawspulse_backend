# Generated by Django 5.0.4 on 2024-04-25 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_pet_help_pet_rename_user_notification_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='help',
            name='pet',
        ),
        migrations.RemoveField(
            model_name='help',
            name='provider',
        ),
        migrations.RemoveField(
            model_name='help',
            name='requester',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='user',
        ),
        migrations.RemoveField(
            model_name='pet_care_diary',
            name='pet',
        ),
        migrations.DeleteModel(
            name='Pet_encyclopedia',
        ),
        migrations.DeleteModel(
            name='Help',
        ),
        migrations.DeleteModel(
            name='Pet',
        ),
        migrations.DeleteModel(
            name='pet_care_diary',
        ),
    ]

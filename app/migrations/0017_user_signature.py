# Generated by Django 5.0.4 on 2024-05-07 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rename_user_id_user_id_remove_user_password_hash_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='signature',
            field=models.CharField(default='一名铲屎官', max_length=255),
            preserve_default=False,
        ),
    ]

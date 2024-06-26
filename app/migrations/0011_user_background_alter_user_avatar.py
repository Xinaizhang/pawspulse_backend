# Generated by Django 5.0.4 on 2024-05-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_help_pet_remove_help_provider_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='background',
            field=models.ImageField(blank=True, null=True, upload_to='user_backgrounds/', verbose_name='背景图片'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_avatars/', verbose_name='用户头像'),
        ),
    ]

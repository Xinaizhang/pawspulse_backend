# Generated by Django 5.0.4 on 2024-04-24 21:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0007_post_created_at_alter_comment_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.RemoveField(
            model_name='like',
            name='User',
        ),
        migrations.RemoveField(
            model_name='post',
            name='User',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='like',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
# Generated by Django 5.0.4 on 2024-04-25 17:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_help_pet_remove_help_provider_and_more'),
        ('community', '0003_delete_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('like_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='点赞创建时间')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='community.post', verbose_name='帖子ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user', verbose_name='用户ID')),
            ],
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='unique_like_post'),
        ),
    ]

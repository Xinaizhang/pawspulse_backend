# Generated by Django 5.0.4 on 2024-04-25 15:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0010_remove_help_pet_remove_help_provider_and_more'),
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Help',
            fields=[
                ('help_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(default=0, verbose_name='互助状态')),
                ('detail', models.TextField(verbose_name='互助详情')),
                ('cost', models.CharField(max_length=255, verbose_name='佣金')),
                ('tags', models.CharField(blank=True, max_length=50, null=True, verbose_name='标签')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet', verbose_name='需要帮助的宠物ID')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help_provided', to='app.user', verbose_name='提供帮助的用户')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help_requests', to='app.user', verbose_name='发布互助的用户')),
            ],
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-25 15:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0010_remove_help_pet_remove_help_provider_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet_encyclopedia',
            fields=[
                ('species_id', models.AutoField(primary_key=True, serialize=False)),
                ('pet_type', models.IntegerField(verbose_name='类别')),
                ('species_name', models.CharField(max_length=255, verbose_name='品种名')),
                ('characteristic', models.TextField(verbose_name='特征')),
                ('care_instruction', models.TextField(verbose_name='护理建议')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('pet_id', models.AutoField(primary_key=True, serialize=False)),
                ('pet_name', models.CharField(max_length=50, verbose_name='宠物名字')),
                ('pet_type', models.IntegerField(verbose_name='类别')),
                ('species_id', models.IntegerField(verbose_name='品种')),
                ('sex', models.IntegerField(verbose_name='性别')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('weight', models.FloatField(verbose_name='体重')),
                ('qr_code', models.CharField(max_length=255, unique=True, verbose_name='宠物身份证二维码')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user', verbose_name='关联的用户ID')),
            ],
        ),
        migrations.CreateModel(
            name='Pet_care_diary',
            fields=[
                ('diary_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='日记内容')),
                ('weight', models.FloatField(verbose_name='宠物体重')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet', verbose_name='关联的宠物ID')),
            ],
        ),
    ]

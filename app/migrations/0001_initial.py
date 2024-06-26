# Generated by Django 5.0.4 on 2024-04-08 02:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PetEncyclopedia',
            fields=[
                ('speciesId', models.AutoField(primary_key=True, serialize=False)),
                ('petType', models.IntegerField()),
                ('speciesName', models.CharField(max_length=255)),
                ('characteristic', models.TextField()),
                ('careInstruction', models.TextField()),
            ],
            options={
                'verbose_name': 'Pet encyclopedia',
                'verbose_name_plural': 'Pet encyclopedias',
            },
        ),
        migrations.CreateModel(
            name='PetFriendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('petFriendId1', models.IntegerField()),
                ('petFriendId2', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Pet friendship',
                'verbose_name_plural': 'Pet friendships',
            },
        ),
        migrations.CreateModel(
            name='PetProfile',
            fields=[
                ('petId', models.AutoField(primary_key=True, serialize=False)),
                ('qrCode', models.CharField(max_length=255)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('petType', models.CharField(choices=[('Cat', '猫'), ('Dog', '狗')], max_length=20)),
                ('speciesId', models.IntegerField()),
                ('age', models.IntegerField()),
                ('weight', models.FloatField()),
            ],
            options={
                'verbose_name': 'Pet profile',
                'verbose_name_plural': 'Pet profiles',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phoneNumber', models.CharField(max_length=15, unique=True)),
                ('passwordHash', models.CharField(max_length=128)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('nickname', models.CharField(max_length=50)),
                ('avatar', models.URLField()),
                ('address', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserFriendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friendId1', models.IntegerField()),
                ('friendId2', models.IntegerField()),
            ],
            options={
                'verbose_name': 'User friendship',
                'verbose_name_plural': 'User friendships',
            },
        ),
        migrations.CreateModel(
            name='PetCareDiary',
            fields=[
                ('diaryId', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('weight', models.FloatField()),
                ('Pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='care_diaries',
                                          to='app.petprofile')),
            ],
            options={
                'verbose_name': 'Pet care diary',
                'verbose_name_plural': 'Pet care diaries',
            },
        ),
        migrations.AddField(
            model_name='petprofile',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet_profiles',
                                    to='app.User'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notificationId', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications',
                                           to='app.User')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'notifications',
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('postId', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_posts',
                                           to='app.User')),
            ],
            options={
                'verbose_name': 'forum post',
                'verbose_name_plural': 'forum posts',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('messageId', models.AutoField(primary_key=True, serialize=False)),
                ('messageContent', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('receiver',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages',
                                   to='app.User')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages',
                                             to='app.User')),
            ],
            options={
                'verbose_name': 'User message',
                'verbose_name_plural': 'User messages',
            },
        ),
        migrations.CreateModel(
            name='WalkService',
            fields=[
                ('serviceId', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Rejected')])),
                ('Pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='walk_services',
                                          to='app.petprofile')),
                ('provider',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provided_walks',
                                   to='app.User')),
                ('requester',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_walks',
                                   to='app.User')),
            ],
            options={
                'verbose_name': 'walk service',
                'verbose_name_plural': 'walk services',
            },
        ),
    ]

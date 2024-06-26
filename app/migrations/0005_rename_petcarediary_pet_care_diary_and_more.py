# Generated by Django 5.0.4 on 2024-04-20 22:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0004_remove_post_userid_help_tags_post_comments_count_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PetCareDiary',
            new_name='pet_care_diary',
        ),
        migrations.RenameModel(
            old_name='PetEncyclopedia',
            new_name='Pet_encyclopedia',
        ),
        migrations.RenameModel(
            old_name='UserFollows',
            new_name='User_follows',
        ),
        migrations.RenameModel(
            old_name='UserMessage',
            new_name='User_message',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='commentId',
            new_name='comment_id',
        ),
        migrations.RenameField(
            model_name='help',
            old_name='helpId',
            new_name='help_id',
        ),
        migrations.RenameField(
            model_name='help',
            old_name='pet_id',
            new_name='Pet',
        ),
        migrations.RenameField(
            model_name='help',
            old_name='provider_id',
            new_name='provider',
        ),
        migrations.RenameField(
            model_name='help',
            old_name='requester_id',
            new_name='requester',
        ),
        migrations.RenameField(
            model_name='Notification',
            old_name='notificationId',
            new_name='notification_id',
        ),
        migrations.RenameField(
            model_name='Notification',
            old_name='userId',
            new_name='User',
        ),
        migrations.RenameField(
            model_name='Pet',
            old_name='petId',
            new_name='pet_id',
        ),
        migrations.RenameField(
            model_name='Pet',
            old_name='petName',
            new_name='pet_name',
        ),
        migrations.RenameField(
            model_name='Pet',
            old_name='petType',
            new_name='pet_type',
        ),
        migrations.RenameField(
            model_name='Pet',
            old_name='qrCode',
            new_name='qr_code',
        ),
        migrations.RenameField(
            model_name='Pet',
            old_name='speciesId',
            new_name='species_id',
        ),
        migrations.RenameField(
            model_name='Pet',
            old_name='userId',
            new_name='User',
        ),
        migrations.RenameField(
            model_name='pet_care_diary',
            old_name='diaryId',
            new_name='diary_id',
        ),
        migrations.RenameField(
            model_name='pet_care_diary',
            old_name='petId',
            new_name='Pet',
        ),
        migrations.RenameField(
            model_name='Pet_encyclopedia',
            old_name='careInstruction',
            new_name='care_instruction',
        ),
        migrations.RenameField(
            model_name='Pet_encyclopedia',
            old_name='petType',
            new_name='pet_type',
        ),
        migrations.RenameField(
            model_name='Pet_encyclopedia',
            old_name='speciesId',
            new_name='species_id',
        ),
        migrations.RenameField(
            model_name='Pet_encyclopedia',
            old_name='speciesName',
            new_name='species_name',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='pictureUrl',
            new_name='picture_url',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='postId',
            new_name='post_id',
        ),
        migrations.RenameField(
            model_name='User',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='User',
            old_name='passwordHash',
            new_name='password_hash',
        ),
        migrations.RenameField(
            model_name='User',
            old_name='phoneNumber',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='User',
            old_name='userId',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='User_follows',
            old_name='followId',
            new_name='follow_id',
        ),
        migrations.RenameField(
            model_name='User_follows',
            old_name='followeeId',
            new_name='followee',
        ),
        migrations.RenameField(
            model_name='User_follows',
            old_name='followerId',
            new_name='follower',
        ),
        migrations.RenameField(
            model_name='User_message',
            old_name='messageContent',
            new_name='message_content',
        ),
        migrations.RenameField(
            model_name='User_message',
            old_name='messageId',
            new_name='message_id',
        ),
        migrations.RenameField(
            model_name='User_message',
            old_name='receiver_id',
            new_name='receiver',
        ),
        migrations.RenameField(
            model_name='User_message',
            old_name='sender_id',
            new_name='sender',
        ),
    ]

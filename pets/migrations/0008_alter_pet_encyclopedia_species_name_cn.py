# Generated by Django 5.0.4 on 2024-05-21 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0007_alter_pet_encyclopedia_care_instruction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet_encyclopedia',
            name='species_name_cn',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='品种中文名'),
        ),
    ]

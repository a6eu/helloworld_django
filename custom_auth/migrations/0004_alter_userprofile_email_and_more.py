# Generated by Django 4.2.10 on 2024-03-03 18:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_alter_userprofile_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(db_index=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(db_index=True, max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Numbers without +7/8', regex='\\d{10}$')]),
        ),
    ]

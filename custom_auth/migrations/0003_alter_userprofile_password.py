# Generated by Django 4.2.10 on 2024-02-19 16:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0002_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Пароль должен быть длиной от 8 до 20 символов, начинаться с буквы и содержать как минимум одну цифру.', regex='^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,20}$')]),
        ),
    ]
# Generated by Django 4.2.11 on 2024-03-06 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0005_passwordresettoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='reset_code',
            field=models.CharField(max_length=7, unique=True),
        ),
    ]

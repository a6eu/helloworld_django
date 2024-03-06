# Generated by Django 4.2.10 on 2024-02-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='logo_url',
            field=models.ImageField(blank=True, null=True, upload_to='01it.group/brands/'),
        ),
    ]
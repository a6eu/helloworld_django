# Generated by Django 4.2.11 on 2024-03-22 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img_file',
            field=models.ImageField(blank=True, null=True, upload_to='01it.group/products/'),
        ),
    ]
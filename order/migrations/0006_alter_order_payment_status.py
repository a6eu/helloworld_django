# Generated by Django 4.2.10 on 2024-03-02 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20240227_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='order.paymentstatus'),
        ),
    ]

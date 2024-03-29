# Generated by Django 4.2.10 on 2024-02-27 11:27

from django.db import migrations


def create_default_payment_statuses(apps, _schema_editor):
    PaymentStatus = apps.get_model('order', 'PaymentStatus')

    PaymentStatus.objects.bulk_create([
        PaymentStatus(status='Cash'),
        PaymentStatus(status='KaspiQr'),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_orderedproducts_price'),
    ]

    operations = [
        migrations.RunPython(create_default_payment_statuses, reverse_code=migrations.RunPython.noop),
    ]

# Generated by Django 4.0.6 on 2022-07-26 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_remove_invoice_delivery_status_invoice_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('Not Packed', 'Not Packed'), ('Ready For Shipment', 'Ready For Shipment'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled'), ('Returned', 'Returned'), ('Replaced', 'Replaced'), ('Failed', 'Failed')], default='Not Packed', max_length=20),
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-22 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_invoice_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='order_status',
            new_name='delivery_status',
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-21 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_customer_age_alter_customer_mobile_no_and_more'),
        ('seller', '0002_product_return_replace_days'),
        ('customer', '0004_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.IntegerField()),
                ('brand_name', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=50)),
                ('buy_price', models.FloatField()),
                ('product_discount', models.IntegerField()),
                ('product_size', models.CharField(max_length=10)),
                ('product_color', models.CharField(max_length=15)),
                ('order_status', models.CharField(choices=[('Not Packed', 'Not Packed'), ('Ready For Shipment', 'Ready For Shipment'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Not Packed', max_length=20)),
                ('order_delivery_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('returned_date', models.DateTimeField()),
                ('returned_reason', models.TextField()),
                ('pick_up_date', models.DateTimeField(blank=True, null=True)),
                ('pick_up_status', models.CharField(choices=[('Will Soon Pick Up the Product', 'Will Soon Pick Up the Product'), ('Pick Up Done', 'Pick Up Done')], default='Will Soon Pick Up the Product', max_length=30)),
                ('refund_status', models.CharField(choices=[('Not Initiated', 'Not Initiated'), ('Initiated', 'Initiated'), ('Done', 'Done')], default='Not Initiated', max_length=20)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='ReplaceProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replaced_date', models.DateTimeField()),
                ('replacement_reason', models.TextField()),
                ('replace_pickup_date', models.DateTimeField(blank=True, null=True)),
                ('replace_pickup_status', models.CharField(choices=[('Will Soon Pick Up the Product', 'Will Soon Pick Up the Product'), ('Pick Up Done', 'Pick Up Done')], default='Will Soon Pick Up the Product', max_length=30)),
                ('replace_delivery_date', models.DateTimeField(blank=True, null=True)),
                ('replace_delivery_status', models.CharField(choices=[('Not Packed', 'Not Packed'), ('Ready For Shipment', 'Ready For Shipment'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Not Packed', max_length=20)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.invoice')),
                ('replace_product_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.colour')),
                ('replace_product_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.size')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('total_amount', models.FloatField()),
                ('payment_method', models.CharField(default='Cash On Delivery', max_length=30)),
                ('order_id', models.CharField(blank=True, default=None, max_length=100, null=True, unique=True)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('payment_status', models.CharField(choices=[('SUCCESS', 'SUCCESS'), ('FAILURE', 'FAILURE'), ('PENDING', 'PENDING')], default='PENDING', max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.order'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.product'),
        ),
    ]

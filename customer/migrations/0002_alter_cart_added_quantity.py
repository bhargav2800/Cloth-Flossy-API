# Generated by Django 4.0.6 on 2022-07-20 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='added_quantity',
            field=models.IntegerField(default=1),
        ),
    ]

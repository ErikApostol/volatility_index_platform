# Generated by Django 2.1.4 on 2018-12-24 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instvol', '0003_stockprice_open_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockprice',
            name='open_price',
        ),
        migrations.RemoveField(
            model_name='stockprice',
            name='price',
        ),
    ]

# Generated by Django 4.1.2 on 2022-11-08 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_variation'),
        ('order', '0002_rename_phone_nember_order_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_order',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product_order',
            name='size',
        ),
        migrations.RemoveField(
            model_name='product_order',
            name='variation',
        ),
        migrations.AddField(
            model_name='product_order',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]

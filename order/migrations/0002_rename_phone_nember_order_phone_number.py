# Generated by Django 4.1.2 on 2022-11-06 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='phone_nember',
            new_name='phone_number',
        ),
    ]

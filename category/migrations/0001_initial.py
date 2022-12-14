# Generated by Django 4.1.2 on 2022-10-09 19:59

import category.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('category_image', models.ImageField(upload_to=category.models.uploaded_photos)),
                ('slug', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
    ]

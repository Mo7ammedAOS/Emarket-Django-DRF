# Generated by Django 4.1.2 on 2022-11-15 16:10

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_reviewrate_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ImageField(upload_to=store.models.uploaded_photos),
        ),
        migrations.CreateModel(
            name='Product_Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=225, upload_to=store.models.uploaded_photos)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]

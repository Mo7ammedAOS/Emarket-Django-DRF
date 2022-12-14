# Generated by Django 4.1.2 on 2022-11-19 18:12

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
        ('store', '0006_alter_product_images_product_gallery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product_gallery',
            options={'verbose_name': 'Product_Gallery', 'verbose_name_plural': 'Product Gallery'},
        ),
        migrations.AddField(
            model_name='reviewrate',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ImageField(upload_to=store.models.uploaded_photos),
        ),
    ]

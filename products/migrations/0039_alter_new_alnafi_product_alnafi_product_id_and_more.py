# Generated by Django 4.1.5 on 2023-10-09 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_new_alnafi_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_alnafi_product',
            name='alnafi_product_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='new_alnafi_product',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

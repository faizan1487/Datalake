# Generated by Django 4.1.5 on 2023-07-06 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0030_alter_main_product_amount_gbp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_product',
            name='product_slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.1.5 on 2023-10-13 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0039_alter_new_alnafi_product_alnafi_product_id_and_more'),
        ('payment', '0057_remove_main_payment_product_main_payment_product'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='main_payment',
        #     name='product',
        # ),
        # migrations.AddField(
        #     model_name='main_payment',
        #     name='product',
        #     field=models.ManyToManyField(blank=True, related_name='product_payments', to='products.main_product'),
        # ),
    ]

# Generated by Django 4.1.5 on 2023-05-10 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0020_rename_product_main_payment_product_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='main_payment',
            old_name='product',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='main_payment',
            old_name='user',
            new_name='user',
        ),
    ]

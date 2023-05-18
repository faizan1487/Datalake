# Generated by Django 4.1.5 on 2023-05-16 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_alter_main_product_id'),
        ('payment', '0022_alter_main_payment_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_payment',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_payments', to='products.main_product'),
        ),
    ]

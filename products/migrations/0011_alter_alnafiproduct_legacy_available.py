# Generated by Django 4.1.5 on 2023-03-14 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alnafiproduct_allow_coupon_alnafiproduct_amount_gbp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alnafiproduct',
            name='legacy_available',
            field=models.BooleanField(default=True),
        ),
    ]

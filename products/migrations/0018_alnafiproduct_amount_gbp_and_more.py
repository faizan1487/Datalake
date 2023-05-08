# Generated by Django 4.1.5 on 2023-03-21 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alnafiproduct_amount_pkr_alnafiproduct_amount_usd'),
    ]

    operations = [
        migrations.AddField(
            model_name='alnafiproduct',
            name='amount_gbp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='legacy_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='legacy_fee_pkr',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='legacy_fee_usd',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='old_amount_pkr',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='old_amount_usd',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

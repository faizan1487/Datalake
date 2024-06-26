# Generated by Django 4.1.5 on 2023-03-21 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_alnafiproduct_amount_gbp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alnafiproduct',
            name='lms_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='qarz_fee_pkr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='qarz_fee_usd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='qarz_product',
            field=models.BooleanField(default=False),
        ),
    ]

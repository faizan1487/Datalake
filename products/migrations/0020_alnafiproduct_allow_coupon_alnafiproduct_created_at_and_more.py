# Generated by Django 4.1.5 on 2023-03-21 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alnafiproduct_lms_id_alnafiproduct_qarz_fee_pkr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alnafiproduct',
            name='allow_coupon',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='has_legacy_version',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alnafiproduct',
            name='is_certificate_product',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.1.5 on 2023-10-03 09:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_delete_new_alnafi_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_Alnafi_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('product_type', models.CharField(blank=True, max_length=255, null=True)),
                ('product_plan', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_pkr', models.CharField(blank=True, max_length=50, null=True)),
                ('amount_usd', models.CharField(blank=True, max_length=50, null=True)),
                ('duration', models.CharField(blank=True, max_length=50, null=True)),
                ('discount_applied_pkr', models.CharField(blank=True, max_length=100, null=True)),
                ('discount_applied_usd', models.CharField(blank=True, max_length=100, null=True)),
                ('price_gbp', models.CharField(blank=True, max_length=100, null=True)),
                ('alnafi_product_id', models.CharField(blank=True, max_length=100, null=True)),
                ('product_language', models.CharField(blank=True, max_length=255, null=True)),
                ('is_certificate_product', models.BooleanField(default=False)),
                ('bundle_ids', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
            ],
            options={
                'verbose_name': 'New Al-Nafi Product',
                'managed': True,
            },
        ),
    ]

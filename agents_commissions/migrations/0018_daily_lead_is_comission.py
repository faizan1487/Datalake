# Generated by Django 4.1.5 on 2024-03-04 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_commissions', '0017_deleted_daily_sales_support_daily_sales_support_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_lead',
            name='is_comission',
            field=models.BooleanField(default=False),
        ),
    ]

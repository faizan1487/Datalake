# Generated by Django 4.1.5 on 2024-01-31 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_commissions', '0009_daily_sales_support'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_lead',
            name='is_exam_fee',
            field=models.CharField(blank=True, max_length=101, null=True),
        ),
    ]

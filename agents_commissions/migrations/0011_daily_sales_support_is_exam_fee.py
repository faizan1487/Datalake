# Generated by Django 4.1.5 on 2024-01-31 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_commissions', '0010_daily_lead_is_exam_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_sales_support',
            name='is_exam_fee',
            field=models.CharField(blank=True, max_length=101, null=True),
        ),
    ]

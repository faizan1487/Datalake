# Generated by Django 4.1.5 on 2024-02-06 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_commissions', '0012_daily_lead_support'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_lead',
            name='completely_verified',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

# Generated by Django 4.1.5 on 2024-01-10 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_commissions', '0004_alter_daily_lead_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_lead',
            name='plan',
            field=models.CharField(blank=True, max_length=101, null=True),
        ),
    ]

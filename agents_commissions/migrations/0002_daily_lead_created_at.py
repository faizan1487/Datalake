# Generated by Django 4.1.5 on 2024-01-10 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_commissions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_lead',
            name='created_at',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

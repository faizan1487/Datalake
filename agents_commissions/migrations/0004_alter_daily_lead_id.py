# Generated by Django 4.1.5 on 2024-01-10 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_commissions', '0003_alter_daily_lead_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_lead',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False, unique=True),
        ),
    ]

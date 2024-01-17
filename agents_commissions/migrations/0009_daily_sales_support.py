# Generated by Django 4.1.5 on 2024-01-17 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_commissions', '0008_rename_al_baseer_verify_daily_lead_manager_approval_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily_Sales_Support',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=101, null=True)),
                ('product', models.CharField(blank=True, max_length=101, null=True)),
                ('plan', models.CharField(blank=True, max_length=101, null=True)),
                ('amount', models.CharField(blank=True, max_length=101, null=True)),
                ('source', models.CharField(blank=True, max_length=101, null=True)),
                ('lead_creator', models.CharField(blank=True, max_length=101, null=True)),
                ('manager_approval', models.CharField(blank=True, max_length=50, null=True)),
                ('manager_approval_crm', models.CharField(blank=True, max_length=50, null=True)),
                ('veriification_cfo', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
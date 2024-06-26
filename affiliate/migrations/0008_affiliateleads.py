# Generated by Django 4.1.5 on 2023-08-01 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0007_alter_affiliateuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliateLeads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('contact', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('erp_lead_id', models.CharField(blank=True, max_length=255, null=True)),
                ('affiliate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='affiliate_leads', to='affiliate.affiliateuser')),
            ],
        ),
    ]

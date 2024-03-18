# Generated by Django 4.1.5 on 2023-06-26 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0004_affiliateuser_erp_lead_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliateuser',
            name='accept_aggrement',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='affiliateuser',
            name='category_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='affiliateuser',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='affiliateuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='affiliateuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='affiliateuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='affiliateuser',
            name='language',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='affiliateuser',
            name='referral_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='affiliateuser',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='affiliateuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

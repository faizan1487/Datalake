# Generated by Django 4.1.5 on 2023-09-27 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0061_remove_alnafi_user_erp_lead_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='alnafi_user',
            name='erp_lead_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

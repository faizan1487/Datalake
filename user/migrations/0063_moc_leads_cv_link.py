# Generated by Django 4.1.5 on 2023-10-05 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0062_alnafi_user_erp_lead_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='moc_leads',
            name='cv_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

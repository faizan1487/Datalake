# Generated by Django 4.1.5 on 2023-06-09 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0033_alter_alnafi_user_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_user',
            name='erp_lead_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
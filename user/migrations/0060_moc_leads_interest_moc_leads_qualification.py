# Generated by Django 4.1.5 on 2023-09-27 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0059_main_user_blocked_main_user_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='moc_leads',
            name='interest',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='moc_leads',
            name='qualification',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
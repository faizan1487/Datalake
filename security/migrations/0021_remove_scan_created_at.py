# Generated by Django 4.1.5 on 2023-07-17 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0020_scan_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scan',
            name='created_at',
        ),
    ]

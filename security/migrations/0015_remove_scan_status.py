# Generated by Django 4.1.5 on 2023-06-16 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0014_scan_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scan',
            name='status',
        ),
    ]

# Generated by Django 4.1.5 on 2023-06-15 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0006_alter_scan_scan_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='scan_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

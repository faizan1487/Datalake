# Generated by Django 4.1.5 on 2023-08-17 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0023_remove_scan_assigned_to_scan_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='media/security/file_uploads'),
        ),
    ]

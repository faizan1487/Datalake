# Generated by Django 4.1.5 on 2023-08-17 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0025_alter_scan_file_upload_alter_scan_poc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='poc',
            field=models.FileField(blank=True, null=True, upload_to='security/poc_uploads'),
        ),
    ]

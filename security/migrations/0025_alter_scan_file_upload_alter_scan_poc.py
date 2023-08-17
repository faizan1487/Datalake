# Generated by Django 4.1.5 on 2023-08-17 11:31

from django.db import migrations, models
import security.models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0024_alter_scan_file_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='security/file_uploads'),
        ),
        migrations.AlterField(
            model_name='scan',
            name='poc',
            field=models.FileField(blank=True, null=True, storage=security.models.YourS3Storage(), upload_to='security/poc_uploads'),
        ),
    ]
# Generated by Django 4.1.5 on 2023-12-18 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secrets_api', '0005_examallsecretsapi_lastlastsecretapiusing'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LastLastSecretApiUsing',
            new_name='ExamLastSecretApiUsing',
        ),
    ]

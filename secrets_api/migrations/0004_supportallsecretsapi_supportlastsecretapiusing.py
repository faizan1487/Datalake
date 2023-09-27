# Generated by Django 4.1.5 on 2023-09-27 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secrets_api', '0003_alter_allsecretsapi_turn_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportAllSecretsApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('turn_number', models.IntegerField(default=1, unique=True)),
                ('api_key', models.CharField(max_length=200, unique=True)),
                ('secret_key', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SupportLastSecretApiUsing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('turn_number', models.IntegerField(default=1)),
                ('api_key', models.CharField(max_length=200, unique=True)),
                ('secret_key', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]

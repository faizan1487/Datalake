# Generated by Django 4.1.5 on 2023-09-07 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secrets_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allsecretsapi',
            name='turn_number',
            field=models.IntegerField(default=1),
        ),
    ]

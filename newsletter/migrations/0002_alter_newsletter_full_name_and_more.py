# Generated by Django 4.1.5 on 2023-06-07 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='phone_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

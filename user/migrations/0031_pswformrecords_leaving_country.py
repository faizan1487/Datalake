# Generated by Django 4.1.5 on 2023-06-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_rename_move_another_eu_country_pswformrecords_move_another_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='pswformrecords',
            name='leaving_country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

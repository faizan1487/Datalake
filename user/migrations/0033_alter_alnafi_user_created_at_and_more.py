# Generated by Django 4.1.5 on 2023-06-08 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0032_rename_leaving_country_pswformrecords_living_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alnafi_user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='main_user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='main_user',
            name='modified_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

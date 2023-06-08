# Generated by Django 4.1.5 on 2023-06-08 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0002_alter_affiliateuser_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='affiliateuniqueclick',
            name='address',
        ),
        migrations.RemoveField(
            model_name='affiliateuniqueclick',
            name='country',
        ),
        migrations.RemoveField(
            model_name='affiliateuniqueclick',
            name='email',
        ),
        migrations.RemoveField(
            model_name='affiliateuniqueclick',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='affiliateuniqueclick',
            name='phone',
        ),
        migrations.AddField(
            model_name='affiliateuniqueclick',
            name='pkr_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='affiliateuniqueclick',
            name='usd_price',
            field=models.IntegerField(default=0),
        ),
    ]

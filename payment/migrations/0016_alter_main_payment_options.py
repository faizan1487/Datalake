# Generated by Django 4.1.5 on 2023-05-08 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_main_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='main_payment',
            options={'managed': True, 'ordering': ['-order_datetime'], 'verbose_name': 'Main Payment'},
        ),
    ]

# Generated by Django 4.1.5 on 2023-02-22 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_alter_easypaisa_payment_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='easypaisa_payment',
            options={'managed': False, 'verbose_name': 'Easypaisa Payment'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'managed': False, 'verbose_name': 'Stripe Payment'},
        ),
        migrations.AlterModelOptions(
            name='ubl_ipg_payment',
            options={'managed': False, 'verbose_name': 'UBL IPG Payment'},
        ),
    ]

# Generated by Django 4.1.5 on 2023-08-04 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0040_alter_alnafi_payment_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alnafi_payment',
            name='payment_id',
            field=models.IntegerField(null=True),
        ),
    ]
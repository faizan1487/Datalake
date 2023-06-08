# Generated by Django 4.1.5 on 2023-03-26 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_stripe_payment_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripe_payment',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='stripe_payment',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='stripe_payment',
            name='product_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
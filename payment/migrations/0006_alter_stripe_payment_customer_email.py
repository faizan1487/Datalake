# Generated by Django 4.1.5 on 2023-03-26 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_stripe_payment_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripe_payment',
            name='customer_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

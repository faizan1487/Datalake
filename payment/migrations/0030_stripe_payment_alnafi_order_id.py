# Generated by Django 4.1.5 on 2023-06-13 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0029_rename_ubl_payment_channel_main_payment_ubl_candidate_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripe_payment',
            name='alnafi_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 4.1.5 on 2023-09-25 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0044_new_al_nafi_payments_customer_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_al_nafi_payments',
            name='source',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]

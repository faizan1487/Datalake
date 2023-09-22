# Generated by Django 4.1.5 on 2023-09-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0043_new_al_nafi_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_al_nafi_payments',
            name='customer_email',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='new_al_nafi_payments',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='new_al_nafi_payments',
            name='orderId',
            field=models.CharField(default='noid', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]

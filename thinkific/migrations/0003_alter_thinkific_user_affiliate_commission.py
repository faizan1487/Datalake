# Generated by Django 4.1.5 on 2023-03-31 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thinkific', '0002_alter_thinkific_user_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thinkific_user',
            name='affiliate_commission',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]

# Generated by Django 4.1.5 on 2023-07-17 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thinkific', '0014_thinkific_user_erp_lead_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thinkific_user',
            name='email',
            field=models.EmailField(default='no email', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]

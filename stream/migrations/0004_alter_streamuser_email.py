# Generated by Django 4.1.5 on 2023-07-24 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0003_streamuser_erp_lead_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamuser',
            name='email',
            field=models.EmailField(default='noemail', max_length=254, unique=True),
            preserve_default=False,
        ),
    ]

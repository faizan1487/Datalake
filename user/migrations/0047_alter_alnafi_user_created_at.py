# Generated by Django 4.1.5 on 2023-07-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0046_alter_alnafi_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alnafi_user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

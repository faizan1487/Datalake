# Generated by Django 4.1.5 on 2023-08-03 10:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatwoot', '0012_alter_conversation_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]

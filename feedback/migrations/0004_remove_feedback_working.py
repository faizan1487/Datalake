# Generated by Django 4.1.5 on 2023-08-16 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_feedback_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='working',
        ),
    ]
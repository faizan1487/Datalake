# Generated by Django 4.1.5 on 2023-05-29 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_alter_main_user_is_paying_customer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='main_user',
            options={'managed': True, 'ordering': ['-created_at'], 'verbose_name': 'Main User'},
        ),
    ]
# Generated by Django 4.1.5 on 2023-04-26 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_alter_navbarlink_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alnafi_user',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

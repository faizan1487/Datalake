# Generated by Django 4.1.5 on 2023-04-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user', '0021_alter_alnafi_user_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='navbarlink',
            name='group',
        ),
        migrations.AddField(
            model_name='navbarlink',
            name='group',
            field=models.ManyToManyField(to='auth.group'),
        ),
    ]
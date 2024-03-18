# Generated by Django 4.1.5 on 2023-09-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0057_alter_new_alnafi_user_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='new_alnafi_user',
            old_name='full_name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='new_alnafi_user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='new_alnafi_user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='new_alnafi_user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='new_alnafi_user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='new_alnafi_user',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='new_alnafi_user',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='new_alnafi_user',
            name='source',
            field=models.CharField(blank=True, default='alnafi.edu.pk', max_length=30, null=True),
        ),
    ]

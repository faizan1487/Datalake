# Generated by Django 4.1.5 on 2023-09-19 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0058_rename_full_name_new_alnafi_user_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_user',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='main_user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='main_user',
            name='easypaisa_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='main_user',
            name='facebook_user_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='main_user',
            name='google_user_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='main_user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='main_user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='main_user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='main_user',
            name='meta_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='main_user',
            name='provider',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='main_user',
            name='student_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='main_user',
            name='student_email_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='main_user',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]

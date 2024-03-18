# Generated by Django 4.1.5 on 2023-04-01 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thinkific', '0008_rename_free_trial_thinkific_users_enrollments_completed_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thinkific_users_enrollments',
            old_name='completed',
            new_name='free_trial',
        ),
        migrations.RemoveField(
            model_name='thinkific_users_enrollments',
            name='course_name',
        ),
        migrations.RemoveField(
            model_name='thinkific_users_enrollments',
            name='email',
        ),
        migrations.RemoveField(
            model_name='thinkific_users_enrollments',
            name='expired',
        ),
        migrations.RemoveField(
            model_name='thinkific_users_enrollments',
            name='is_free_trial',
        ),
        migrations.RemoveField(
            model_name='thinkific_users_enrollments',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='thinkific_users_enrollments',
            name='username',
        ),
        migrations.AddField(
            model_name='thinkific_users_enrollments',
            name='course_details',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thinkific_users_enrollments',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thinkific_users_enrollments',
            name='user_details',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

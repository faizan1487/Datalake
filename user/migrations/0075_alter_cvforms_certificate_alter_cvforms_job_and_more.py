# Generated by Django 4.1.5 on 2023-12-22 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0074_rename_academic_qualification_cvforms_job_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvforms',
            name='certificate',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cvforms',
            name='job',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cvforms',
            name='qualification',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cvforms',
            name='refrences',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cvforms',
            name='skills',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cvforms',
            name='work_history',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

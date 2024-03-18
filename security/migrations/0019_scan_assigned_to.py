# Generated by Django 4.1.5 on 2023-07-17 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0018_remove_comment_department_remove_scan_assigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_scans', to='security.department'),
        ),
    ]

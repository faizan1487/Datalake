# Generated by Django 4.1.5 on 2023-03-15 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alnafiuser_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='alnafiuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

# Generated by Django 4.1.5 on 2023-12-15 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={},
        ),
        migrations.AlterField(
            model_name='expense',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]

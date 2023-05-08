# Generated by Django 4.1.5 on 2023-04-07 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_navbarlink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='navbarlink',
            name='slug',
        ),
        migrations.AddField(
            model_name='navbarlink',
            name='path',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='navbarlink',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

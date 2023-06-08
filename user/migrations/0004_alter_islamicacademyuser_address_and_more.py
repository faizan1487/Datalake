# Generated by Django 4.1.5 on 2023-03-10 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_islamicacademyuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='islamicacademyuser',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='islamicacademyuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='islamicacademyuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='islamicacademyuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='islamicacademyuser',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='islamicacademyuser',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
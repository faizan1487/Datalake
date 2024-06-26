# Generated by Django 4.1.5 on 2023-04-08 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavbarLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('path', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(upload_to='navbar_images')),
                ('group', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]

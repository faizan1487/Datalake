# Generated by Django 4.1.5 on 2023-05-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_remove_navbarlink_group_navbarlink_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Main_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('source', models.CharField(blank=True, choices=[('AlNafi_User', 'AlNafi User'), ('IslamicAcademy_User', 'Islamic Academy User')], max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('language', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(blank=True, null=True)),
                ('verification_code', models.CharField(blank=True, max_length=30, null=True)),
                ('isAffiliate', models.BooleanField(default=False)),
                ('how_did_you_hear_about_us', models.CharField(blank=True, max_length=255, null=True)),
                ('affiliate_code', models.CharField(blank=True, max_length=255, null=True)),
                ('isMentor', models.BooleanField(default=False)),
                ('is_paying_customer', models.BooleanField(default=False)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Main User',
                'managed': True,
            },
        ),
    ]
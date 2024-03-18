# Generated by Django 4.1.5 on 2023-03-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_islamicacademyuser_is_paying_customer'),
    ]

    operations = [
        migrations.CreateModel( 
            name='AlnafiUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=25, null=True)),
                ('address', models.TextField(null=True)),
                ('country', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255, null=True)),
                ('verification_code', models.CharField(max_length=30)),
                ('isAffiliate', models.BooleanField(default=False)),
                ('how_did_you_hear_about_us', models.CharField(max_length=255, null=True)),
                ('affiliate_code', models.CharField(max_length=255, null=True)),
                ('isMentor', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Al-Nafi User',
                'managed': True,
            },
        ),
        # migrations.RenameModel(
        #     old_name='User',
        #     new_name='User1'
        # ),
    ]

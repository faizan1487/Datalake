# Generated by Django 4.1.5 on 2023-04-07 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_alter_ubl_manual_payment_activation_datetime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavbarLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(upload_to='navbar_images')),
            ],
        ),
    ]

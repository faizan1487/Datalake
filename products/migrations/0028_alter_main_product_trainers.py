# Generated by Django 4.1.5 on 2023-05-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0001_initial'),
        ('products', '0027_main_product_trainers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_product',
            name='trainers',
            field=models.ManyToManyField(blank=True, null=True, to='trainers.trainer'),
        ),
    ]

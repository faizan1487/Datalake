# Generated by Django 4.1.5 on 2023-05-31 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0002_alter_trainer_products'),
        ('products', '0028_alter_main_product_trainers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_product',
            name='trainers',
            field=models.ManyToManyField(to='trainers.trainer'),
        ),
    ]

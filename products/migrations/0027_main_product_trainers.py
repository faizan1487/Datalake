# Generated by Django 4.1.5 on 2023-05-30 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0001_initial'),
        ('products', '0026_alter_main_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_product',
            name='trainers',
            field=models.ManyToManyField(to='trainers.trainer'),
        ),
    ]

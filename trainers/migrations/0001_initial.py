# Generated by Django 4.1.5 on 2023-05-30 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0026_alter_main_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainer_name', models.CharField(max_length=255)),
                ('products', models.ManyToManyField(to='products.main_product')),
            ],
            options={
                'verbose_name': 'Trainer',
                'managed': True,
            },
        ),
    ]

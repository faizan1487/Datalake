# Generated by Django 4.1.5 on 2023-08-16 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_remove_track_includedcourses'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='includedCourses',
            field=models.ManyToManyField(to='products.course'),
        ),
    ]

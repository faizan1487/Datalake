# Generated by Django 4.1.5 on 2023-08-16 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0007_feedbackquestion_feedbackanswers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackanswers',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
# Generated by Django 4.1.5 on 2023-10-16 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0063_moc_leads_cv_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moc_leads',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True,blank=True),
            preserve_default=False,
        ),
    ]

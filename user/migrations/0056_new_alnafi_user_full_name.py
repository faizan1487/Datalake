# Generated by Django 4.1.5 on 2023-09-13 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0055_moc_leads_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_alnafi_user',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
# Generated by Django 4.1.5 on 2023-06-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0035_alnafi_user_erp_lead_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pswformrecords',
            old_name='contact_number',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='pswformrecords',
            old_name='email_address',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='pswformrecords',
            old_name='full_name',
            new_name='first_name',
        ),
        migrations.RemoveField(
            model_name='pswformrecords',
            name='living_country',
        ),
        migrations.AddField(
            model_name='pswformrecords',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

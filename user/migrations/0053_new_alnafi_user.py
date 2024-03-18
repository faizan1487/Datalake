# Generated by Django 4.1.5 on 2023-09-11 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0052_rename_address_moc_leads_form_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_AlNafi_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('student_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('student_email_status', models.CharField(blank=True, max_length=50, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('meta_data', models.JSONField(blank=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics')),
                ('facebook_user_id', models.CharField(blank=True, max_length=50, null=True)),
                ('google_user_id', models.CharField(blank=True, max_length=50, null=True)),
                ('provider', models.CharField(blank=True, max_length=50, null=True)),
                ('affiliate_code', models.CharField(blank=True, max_length=30, null=True)),
                ('source', models.CharField(blank=True, default='alnafi.com', max_length=30, null=True)),
                ('easypaisa_number', models.CharField(blank=True, max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]

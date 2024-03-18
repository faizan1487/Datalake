# Generated by Django 4.1.5 on 2024-03-18 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0077_moc_leads_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testing_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('internal_source', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('language', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('verification_code', models.CharField(blank=True, max_length=30, null=True)),
                ('isAffiliate', models.BooleanField(default=False)),
                ('how_did_you_hear_about_us', models.CharField(blank=True, max_length=255, null=True)),
                ('affiliate_code', models.CharField(blank=True, max_length=255, null=True)),
                ('isMentor', models.BooleanField(default=False)),
                ('is_paying_customer', models.BooleanField(default=False)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
                ('erp_lead_id', models.CharField(blank=True, max_length=255, null=True)),
                ('student_email', models.CharField(blank=True, max_length=255, null=True)),
                ('student_email_status', models.CharField(blank=True, max_length=50, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('meta_data', models.JSONField(blank=True, null=True)),
                ('facebook_user_id', models.CharField(blank=True, max_length=50, null=True)),
                ('google_user_id', models.CharField(blank=True, max_length=50, null=True)),
                ('provider', models.CharField(blank=True, max_length=50, null=True)),
                ('easypaisa_number', models.CharField(blank=True, max_length=15, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('academy_demo_access', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Test User',
                'ordering': ['-created_at'],
                'managed': True,
            },
        ),
    ]

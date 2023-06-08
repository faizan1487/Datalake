# Generated by Django 4.1.5 on 2023-06-07 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affiliateuser',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='affiliateuser',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='affiliateuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='affiliateuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='affiliateuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='affiliateuser',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='AffiliateUniqueClick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=100, null=True)),
                ('page_url', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('affiliate_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_clicks', to='affiliate.affiliateuser')),
            ],
            options={
                'verbose_name_plural': 'AffiliateUniqueClicks',
            },
        ),
    ]
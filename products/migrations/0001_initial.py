# Generated by Django 4.1.5 on 2023-03-09 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlnafiProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('course', 'Course'), ('track', 'Track'), ('academy', 'academy'), ('other', 'Other')], default='course', max_length=20)),
                ('productSlug', models.CharField(blank=True, max_length=50, null=True)),
                ('plan', models.CharField(choices=[('Monthly', 'Monthly'), ('2 Months', '2 Months'), ('Quarterly', 'Quarterly'), ('Half Yearly', 'Half Yearly'), ('Yearly', 'Yearly'), ('18 Months', '18 Months'), ('24 Months', '24 Months')], default='Yearly', max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('bundle_Ids', models.CharField(blank=True, max_length=200, null=True)),
                ('amount_pkr', models.IntegerField(default=0)),
                ('amount_usd', models.IntegerField(default=0)),
                ('old_amount_pkr', models.IntegerField(default=0)),
                ('old_amount_usd', models.IntegerField(default=0)),
                ('legacy_fee_pkr', models.IntegerField(blank=True, null=True)),
                ('legacy_fee_usd', models.IntegerField(blank=True, null=True)),
                ('legacy_available', models.BooleanField(default=False)),
                ('qarz_product', models.BooleanField(default=False)),
                ('qarz_fee_pkr', models.IntegerField(blank=True, null=True)),
                ('qarz_fee_usd', models.IntegerField(blank=True, null=True)),
                ('lms_id', models.CharField(blank=True, max_length=10, null=True)),
                ('language', models.CharField(default='urdu', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('has_legacy_version', models.BooleanField(default=False)),
            ],
        ),
    ]
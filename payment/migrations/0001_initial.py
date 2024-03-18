# Generated by Django 4.1.5 on 2023-03-25 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Easypaisa_Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ops_id', models.CharField(blank=True, max_length=50, null=True)),
                ('product_name', models.CharField(blank=True, max_length=200, null=True)),
                ('order_id', models.CharField(blank=True, max_length=50, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=50, null=True)),
                ('order_datetime', models.DateTimeField(default=None)),
                ('customer_msidn', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('amount', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('source', models.CharField(blank=True, max_length=50, null=True)),
                ('credit_card', models.CharField(blank=True, max_length=50, null=True)),
                ('bin_bank_name', models.CharField(blank=True, max_length=50, null=True)),
                ('fee_pkr', models.CharField(blank=True, max_length=50, null=True)),
                ('fed_pkr', models.CharField(blank=True, max_length=50, null=True)),
                ('error_reason', models.CharField(blank=True, max_length=200, null=True)),
                ('token_paid_datetime', models.DateTimeField(default=None)),
            ],
            options={
                'verbose_name': 'Easypaisa Payment',
                'ordering': ['-order_datetime'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Stripe_Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=50, null=True)),
                ('order_datetime', models.DateTimeField(blank=True, max_length=60, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('currency', models.CharField(blank=True, max_length=50, null=True)),
                ('source', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name': 'Stripe Payment',
                'ordering': ['-order_datetime'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UBL_IPG_Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=50)),
                ('customer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('card_mask', models.CharField(blank=True, max_length=100, null=True)),
                ('product_name', models.CharField(blank=True, max_length=50, null=True)),
                ('order_datetime', models.DateTimeField(max_length=60)),
                ('order_id', models.CharField(max_length=100)),
                ('amount', models.CharField(blank=True, max_length=50, null=True)),
                ('captured', models.CharField(blank=True, max_length=50, null=True)),
                ('reversed', models.CharField(blank=True, max_length=50, null=True)),
                ('refund', models.CharField(blank=True, max_length=50, null=True)),
                ('approval_code', models.CharField(blank=True, max_length=50, null=True)),
                ('source', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'UBL IPG Payment',
                'ordering': ['-order_datetime'],
                'managed': True,
            },
        ),
    ]

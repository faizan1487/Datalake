# Generated by Django 4.1.5 on 2024-01-31 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0098_main_product_discount_applied_pkr_and_more'),
        ('payment', '0116_new_alnafi_payments_delete_new_al_nafi_payments_and_more'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='New_Alnafi_Payments',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('orderId', models.CharField(max_length=255)),
        #         ('amount', models.IntegerField(blank=True, null=True)),
        #         ('status', models.CharField(blank=True, max_length=255, null=True)),
        #         ('updated_at', models.DateTimeField(blank=True, null=True)),
        #         ('card_number', models.CharField(blank=True, max_length=255, null=True)),
        #         ('account_number', models.CharField(blank=True, max_length=255, null=True)),
        #         ('meta', models.JSONField(blank=True, null=True)),
        #         ('payment_method_name', models.CharField(blank=True, max_length=255, null=True)),
        #         ('payment_method_currency', models.CharField(blank=True, max_length=255, null=True)),
        #         ('payment_method_source_name', models.CharField(blank=True, max_length=255, null=True)),
        #         ('product_names', models.JSONField(blank=True, null=True)),
        #         ('username', models.CharField(blank=True, max_length=200, null=True)),
        #         ('country', models.CharField(blank=True, max_length=255, null=True)),
        #         ('pk_invoice_number', models.CharField(blank=True, max_length=255, null=True)),
        #         ('us_invoice_number', models.CharField(blank=True, max_length=255, null=True)),
        #         ('send_invoice', models.BooleanField(default=False)),
        #         ('purpose', models.CharField(blank=True, max_length=255, null=True)),
        #         ('depositor_name', models.CharField(blank=True, max_length=255, null=True)),
        #         ('application_id', models.CharField(blank=True, max_length=255, null=True)),
        #         ('customer_email', models.CharField(blank=True, max_length=300, null=True)),
        #         ('expiration_date', models.DateTimeField(blank=True, null=True)),
        #         ('coupon_id', models.CharField(blank=True, max_length=255, null=True)),
        #         ('additional_months', models.IntegerField(blank=True, null=True)),
        #         ('is_manual', models.BooleanField(default=False)),
        #         ('amount_pkr', models.IntegerField(blank=True, null=True)),
        #         ('amount_usd', models.IntegerField(blank=True, null=True)),
        #         ('webhook_called', models.BooleanField(default=False)),
        #         ('old_payments', models.IntegerField(blank=True, null=True)),
        #         ('remarks', models.CharField(blank=True, max_length=1000, null=True)),
        #         ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
        #         ('payment_date', models.DateTimeField(blank=True, null=True)),
        #         ('created_at', models.DateTimeField(blank=True, null=True)),
        #     ],
        #     options={
        #         'verbose_name': 'New Al-Nafi Payment',
        #         'managed': True,
        #     },
        # ),
        # migrations.DeleteModel(
        #     name='New_Al_Nafi_Payments',
        # ),
        # migrations.AddField(
        #     model_name='main_payment',
        #     name='product',
        #     field=models.ManyToManyField(blank=True, related_name='product_payments', to='products.main_product'),
        # ),
    ]
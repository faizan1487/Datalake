# Generated by Django 4.1.5 on 2023-03-16 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_alter_alnafiproduct_amount_gbp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alnafiproduct',
            name='allow_coupon',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='amount_gbp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='amount_pkr',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='amount_usd',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='bundle_Ids',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='courses',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/products'),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='language',
            field=models.CharField(default='urdu', max_length=100),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='legacy_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='legacy_fee_pkr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='legacy_fee_usd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='lms_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='old_amount_pkr',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='old_amount_usd',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='plan',
            field=models.CharField(default='Yearly', max_length=20),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='productSlug',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='product_type',
            field=models.CharField(default='course', max_length=20),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='qarz_fee_pkr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alnafiproduct',
            name='qarz_fee_usd',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

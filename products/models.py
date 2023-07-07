from django.db import models
from trainers.models import *
# Create your models here.

# FOR AL-NAFI MAIN SITE PRODUCT:


class Alnafi_Product(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    product_type = models.CharField(max_length=255, null=True, blank=True)
    product_slug = models.CharField(max_length=255, null=True, blank=True)
    plan = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    bundle_Ids = models.CharField(max_length=255, null=True, blank=True)
    amount_pkr = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    amount_usd = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    amount_gbp = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    old_amount_pkr = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    old_amount_usd = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    legacy_fee_pkr = models.IntegerField(default=0, null=True, blank=True)
    legacy_fee_usd = models.IntegerField(default=0, null=True, blank=True)
    legacy_available = models.BooleanField(default=False)
    qarz_product = models.BooleanField(default=False)
    qarz_fee_pkr = models.IntegerField(null=True, blank=True)
    qarz_fee_usd = models.IntegerField(null=True, blank=True)
    lms_id = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    has_legacy_version = models.BooleanField(default=False)
    is_certificate_product = models.BooleanField(default=False)
    allow_coupon = models.BooleanField(default=False)
    courses = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"name {self.name}"

    class Meta:
        managed = True
        verbose_name = "Al-Nafi Product"


# FOR ISLAMIC ACADEMY PRODUCT:
class IslamicAcademy_Product(models.Model):
    TYPE_CHOICES = (
        ('simple', 'Simple'),
        ('variable', 'Variable'),
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
    )
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    product_slug = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default='simple')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='draft')
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_status = models.CharField(max_length=20, default='instock')

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = "Islamic Academy Product"


# FOR MAIN PRODUCTS COMBINE PRODUCT ALL TABLE IN ONE:
class Main_Product(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
    )
    trainers = models.ManyToManyField('trainers.Trainer')
    source = models.CharField(max_length=20, null=True, blank=True)
    product_name = models.CharField(max_length=255,null=True, blank=True)
    product_slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    product_type = models.CharField(max_length=250,null=True, blank=True)
    product_plan = models.CharField(max_length=250,null=True, blank=True)
    amount_pkr = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    amount_gbp = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True, blank=True)
    old_amount_pkr = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True, blank=True)
    old_amount_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True, blank=True)
    legacy_fee_pkr = models.IntegerField(default=0, null=True, blank=True)
    legacy_fee_usd = models.IntegerField(default=0, null=True, blank=True)
    legacy_available = models.BooleanField(default=False)
    qarz_product = models.BooleanField(default=False)
    qarz_fee_pkr = models.IntegerField(null=True, blank=True)
    qarz_fee_usd = models.IntegerField(null=True, blank=True)
    lms_id = models.CharField(max_length=255, null=True, blank=True)
    product_language = models.CharField(max_length=255, null=True, blank=True)
    has_legacy_version = models.BooleanField(default=False)
    is_certificate_product = models.BooleanField(default=False)
    allow_coupon = models.BooleanField(default=False)
    courses = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    bundle_ids = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    description = models.CharField(max_length=255, null=True, blank=True)
    stock_status = models.CharField(max_length=20, default='instock')

    def __str__(self):
        return self.product_name

    class Meta:
        managed = True
        verbose_name = "Main Product"

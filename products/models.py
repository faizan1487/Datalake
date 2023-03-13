from django.db import models

# Create your models here.

#FOR AL-NAFI MAIN SITE PRODUCT:
class AlnafiProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.URLField()
    product_type = models.CharField(max_length=255)
    productSlug = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    bundle_Ids = models.CharField(max_length=255)
    amount_pkr = models.DecimalField(max_digits=10, decimal_places=2)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    amount_gbp = models.DecimalField(max_digits=10, decimal_places=2)
    old_amount_pkr = models.DecimalField(max_digits=10, decimal_places=2)
    old_amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    legacy_fee_pkr = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    legacy_fee_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    legacy_available = models.BooleanField()
    qarz_product = models.BooleanField()
    qarz_fee_pkr = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qarz_fee_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    lms_id = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    has_legacy_version = models.BooleanField()
    is_certificate_product = models.BooleanField()
    allow_coupon = models.BooleanField()
    courses = models.JSONField()

    def __str__(self):
        return self.name
    
    class Meta:
        managed = True
        verbose_name = "Al-Nafi Product"


#FOR ISLAMIC ACADEMY PRODUCT:
class IslamicAcademyProduct(models.Model):
    TYPE_CHOICES = (
        ('simple', 'Simple'),
        ('variable', 'Variable'),
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
    )
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='simple')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_status = models.CharField(max_length=20, default='instock')

    class Meta:
        managed = True
        verbose_name = "Islamic Academy Product"

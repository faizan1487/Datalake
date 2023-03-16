from django.db import models

# Create your models here.

#FOR AL-NAFI MAIN SITE PRODUCT:
class AlnafiProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.ImageField(null=True, blank=True,upload_to='media/products')
    product_type = models.CharField(max_length=20, default='course')
    productSlug = models.CharField(max_length=50, blank=True, null=True)
    plan = models.CharField(max_length=20, default='Yearly')
    name = models.CharField(max_length=100)
    bundle_Ids = models.CharField(max_length=200, null=True, blank=True)
    amount_pkr = models.IntegerField(default=0)
    amount_usd = models.IntegerField(default=0)
    amount_gbp = models.IntegerField(default=0)
    old_amount_pkr = models.IntegerField(default=0)
    old_amount_usd = models.IntegerField(default=0)
    legacy_fee_pkr = models.IntegerField(blank=True, null=True)
    legacy_fee_usd = models.IntegerField(blank=True, null=True)
    legacy_available = models.BooleanField(default=False)
    qarz_product = models.BooleanField(default=False)
    qarz_fee_pkr = models.IntegerField(blank=True, null=True)
    qarz_fee_usd = models.IntegerField(blank=True, null=True)
    lms_id = models.CharField(max_length=10,blank=True, null=True)
    language = models.CharField(max_length=100, default="urdu")
    created_at= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    has_legacy_version = models.BooleanField(default=False)
    is_certificate_product = models.BooleanField(default=False)
    allow_coupon = models.BooleanField(default=True)
    courses = models.CharField(max_length=100,null=True, blank=True)
    
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

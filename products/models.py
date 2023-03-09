from django.db import models

# Create your models here.
#FOR PRODUCT:
class AlnafiProduct(models.Model):
    # image = models.ImageField(null=True, blank=True,
    #                           upload_to='media/products', default="https://import.cdn.thinkific.com/212959/IbhpMoPT4WPwllrOflEp_logo_transperant_png")
    TYPE_CHOICES = (('course', 'Course'), ('track', 'Track'),
                    ('academy', 'academy'), ('other', 'Other'))
    product_type = models.CharField(
        choices=TYPE_CHOICES, max_length=20, default='course')
    productSlug = models.CharField(max_length=50, blank=True, null=True)
    PLANS_CHOICES = [('Monthly', 'Monthly'), ('2 Months', '2 Months'), ('Quarterly', 'Quarterly'),
                     ('Half Yearly', 'Half Yearly'), ('Yearly', 'Yearly'),('18 Months','18 Months'),('24 Months','24 Months')]
    plan = models.CharField(choices=PLANS_CHOICES,
                            max_length=20, default='Yearly')
    name = models.CharField(max_length=100)
    bundle_Ids = models.CharField(max_length=200, null=True, blank=True)

    amount_pkr = models.IntegerField(default=0)
    amount_usd = models.IntegerField(default=0)
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

    def days(self):
        days = 30
        if self.plan.lower() == "yearly" or self.plan.lower() == "annual":
            days = 365
            payments_for_number_of_months += 12
        elif self.plan.lower() == "half yearly":
            days = 182
        elif self.plan.lower() == "quarterly":
            days = 91
        return days

    def __str__(self):
        return self.name
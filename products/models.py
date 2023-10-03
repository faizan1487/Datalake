from django.db import models
from trainers.models import *
from datetime import timezone, datetime
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
        return f"{self.name}"

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
    duration = models.CharField(max_length=50, null=True, blank=True)
    discount_applied_pkr = models.CharField(max_length=100, blank=True, null=True)
    discount_applied_usd = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.product_name}"

    class Meta:
        managed = True
        verbose_name = "Main Product"



class Course(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to='media/courses')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    punchline = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    popular = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    availableForPakistan = models.BooleanField(default=True)
    availableForOverseas = models.BooleanField(default=True)
    languages = models.TextField(blank=True, null=True, default="Urdu")

    category_choices = (("academy", "Academy"), ("course",
                        "Course"), ("asad-zaman", "Asad Zaman"),)
    category = models.CharField(
        max_length=100, choices=category_choices, default="course")
    demo_id = models.IntegerField(blank=True, null=True)
    english_demo_id = models.IntegerField(blank=True, null=True)
    urdu_demo_link = models.CharField(max_length=100, blank=True, null=True)
    english_demo_link = models.CharField(max_length=100, blank=True, null=True)
    demo_duration = models.IntegerField(default=7)
    number_of_demo_users = models.IntegerField(default=0)
    free_course = models.BooleanField(default=False)
    key_features = models.JSONField(blank=True, null=True)

    mata_title = models.CharField(max_length=50, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    search_tags = models.TextField(blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    video = models.URLField(blank=True,null=True)

    level_choices = (("basic", 'Basic'), ('intermediate', 'Intermediate'),
                     ('advance', "Advance"), ('master', 'Master'))
    course_level = models.CharField(
        max_length=100, choices=level_choices, blank=True, null=True, default="intermediate")
    course_priority = models.IntegerField(default=0,null=True,blank=True)
    track_priority = models.CharField(max_length=10,blank=True,null=True)
    # amount_pkr = models.IntegerField(null=True,blank=True)
    rating = models.FloatField(default=4.5)
    reviews = models.IntegerField(default=200)
    number_of_students = models.IntegerField(default=200)

    def __str__(self):
        return self.name

    def amount_pkr(self):
        if self.product:
            return self.product.amount_pkr
        else:
            return 0
    # class Meta:
    #     verbose_name_plural = "List"




class Track(models.Model):
    includedCourses = models.ManyToManyField(Course)
    image = models.ImageField(blank=True, null=True, upload_to='media/tracks')
    name = models.CharField(max_length=100)
    productSlug = models.CharField(
        max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    punchline = models.TextField(max_length=600, blank=True, null=True)
    duration = models.CharField(max_length=250, blank=True, null=True)
    languages = models.TextField(blank=True, null=True, default="Urdu")
    thumbnail = models.ImageField(
        blank=True, null=True, upload_to='media/tracks/thubnails')
    promoVideo = models.FileField(
        blank=True, null=True, upload_to='media/tracks/promoVideos')
    overviewVideoEmbed = models.URLField(blank=True, null=True)
    infographicsImage = models.ImageField(blank=True, null=True)
    multipleInfographic = models.JSONField(blank=True, null=True)
    multipleInfographicAvailable = models.BooleanField(default=False)
    prerequisite = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    what_you_will_learn = models.TextField(blank=True, null=True)
    Career_Opportunities = models.JSONField(blank=True, null=True)
    what_will_you_learn = models.JSONField(blank=True, null=True)
    whyStudy = models.TextField(blank=True, null=True)
    why_study = models.JSONField(blank=True, null=True)
    whyStudyImage = models.ImageField(
        blank=True, null=True, upload_to='media/tracks')
    track_banner = models.ImageField(
        blank=True, null=True, upload_to='media/tracks/banners')
    hasGhanimah = models.BooleanField(default=True)
    hasQarz = models.BooleanField(default=False)

    skills = models.JSONField(blank=True, null=True)
    coggles = models.TextField(blank=True, null=True)

    extraCallToActions = models.TextField(blank=True, null=True)
    demo_id = models.IntegerField(blank=True, null=True)
    english_demo_id = models.IntegerField(blank=True, null=True)
    urdu_demo_link = models.CharField(max_length=100, blank=True, null=True)
    english_demo_link = models.CharField(max_length=100, blank=True, null=True)
    demo_duration = models.IntegerField(default=7)
    number_of_demo_users = models.IntegerField(default=0)

    popular = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    availableForPakistan = models.BooleanField(default=True)
    availableForOverseas = models.BooleanField(default=True)

    plansInfo = models.JSONField(blank=True, null=True)
    mata_title = models.CharField(max_length=50, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    what_you_will_learn = models.TextField(blank=True, null=True)
    Career_Opportunities = models.JSONField(blank=True, null=True)
    mindly_data = models.JSONField(blank=True, null=True)
    hands_on_learning = models.TextField(blank=True, null=True)
    build_expertise = models.TextField(blank=True, null=True)
    scalability_for_larger_teams  = models.TextField(blank=True, null=True)
    dedicated_bussiness_support  = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    mindly_image = models.ImageField(
        blank=True, null=True, upload_to='media/tracks/mindly_images')
    track_priority = models.IntegerField(default=0)
    combo_track = models.BooleanField(default=False)
    has_discount = models.BooleanField(default=True)
    has_legacy_version = models.BooleanField(default=False)
    only_renewals_allowed = models.BooleanField(default=False)
    upgraded_product_slug = models.CharField(
        max_length=100, blank=True, null=True)
    legacy_product_slug = models.CharField(
        max_length=100, blank=True, null=True)
    has_certification = models.BooleanField(
        default=False, blank=True, null=True)
    number_of_students = models.IntegerField(default=100)


    # def certificate_price(self):
    #     if not self.has_certification:
    #         return None
    #     return Certificate.objects.get(track=self).certification_product.amount_gbp


    def __str__(self):
        return self.name
    

# For Al-Nafi New Main Site Product:
class New_Alnafi_Product(models.Model):
    product_name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    product_type = models.CharField(max_length=255, null=True, blank=True)
    product_plan = models.CharField(max_length=255, null=True, blank=True)
    amount_pkr = models.CharField(max_length=50, null=True, blank=True)
    amount_usd = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
    discount_applied_pkr = models.CharField(max_length=100, blank=True, null=True)
    discount_applied_usd = models.CharField(max_length=100, blank=True, null=True)
    price_gbp = models.CharField(max_length=100, blank=True, null=True)
    alnafi_product_id = models.CharField(max_length=100, null=True, blank=True)
    product_language = models.CharField(max_length=255, blank=True, null=True)
    is_certificate_product = models.BooleanField(default=False)
    bundle_ids = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, null=True, blank=True)

    def _str_(self):
        return f"name {self.product_name}"

    class Meta:
        managed = True
        verbose_name = "New Al-Nafi Product"
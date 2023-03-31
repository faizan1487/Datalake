from django.db import models

# Create your models here.
class Thinkific_User(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    roles = models.JSONField(null=True, blank=True)
    avatar_url = models.URLField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    headline = models.CharField(max_length=255, null=True, blank=True)
    affiliate_code = models.CharField(max_length=255, null=True, blank=True)
    external_source = models.CharField(max_length=255, null=True, blank=True)
    affiliate_commission = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    affiliate_commission_type = models.CharField(max_length=255, null=True, blank=True)
    affiliate_payout_email = models.EmailField(max_length=255, null=True, blank=True)
    administered_course_ids = models.JSONField(default=list, null=True, blank=True)
    custom_profile_fields = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return self.email
    
    class Meta:
        managed = True
        verbose_name = "Thinkific User"
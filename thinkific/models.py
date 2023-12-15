from email.policy import default
from django.db import models

# Create your models here.
class Thinkific_User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    roles = models.JSONField(null=True, blank=True)
    avatar_url = models.URLField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    headline = models.CharField(max_length=255, null=True, blank=True)
    affiliate_code = models.CharField(max_length=255, null=True, blank=True)
    external_source = models.CharField(max_length=255, null=True, blank=True)
    affiliate_commission = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    affiliate_commission_type = models.CharField(max_length=255, null=True, blank=True)
    affiliate_payout_email = models.EmailField(max_length=255, null=True, blank=True)
    administered_course_ids = models.JSONField(null=True, blank=True)
    custom_profile_fields = models.JSONField(null=True, blank=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)


    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        managed = True
        verbose_name = "Thinkific User"
        
        
class Thinkific_Users_Enrollments(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True) 
    percentage_completed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    free_trial = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    # thinkific_user_id = models.IntegerField(null=True, blank=True)
    user_id =  models.ForeignKey(Thinkific_User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_enrollments")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    course_id = models.IntegerField(null=True, blank=True)
    course_name = models.CharField(max_length=255, null=True, blank=True)
    completed = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email}"
    class Meta:
        managed = True
        verbose_name = "Thinkific Users Enrollment"
from django.db import models

# Create your models here.
class AffiliateUser(models.Model):
    first_name = models.CharField(max_length=100 , null=True , blank=True)
    last_name = models.CharField(max_length=100 , null=True , blank=True)
    email = models.EmailField(unique=True , null=True , blank=True)
    phone = models.CharField(max_length=100 , null=True , blank=True)
    address = models.CharField(max_length=100 , null=True , blank=True)
    country = models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "AffiliateUsers"



class AffiliateUniqueClick(models.Model):
    ip = models.CharField(max_length=100 , null=True , blank=True)
    page_url = models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    affiliate_id = models.ForeignKey(AffiliateUser, on_delete=models.SET_NULL, null=True, related_name="user_clicks")
    pkr_price = models.IntegerField(default=0)
    usd_price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.ip
    
    class Meta:
        verbose_name_plural = "AffiliateUniqueClicks"
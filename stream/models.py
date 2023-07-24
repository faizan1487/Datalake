from django.db import models
# Create your models here.
class StreamUser(models.Model):
    first_name = models.CharField(max_length=100 , null=True , blank=True)
    last_name = models.CharField(max_length=100 , null=True , blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100 , null=True , blank=True)
    phone = models.CharField(max_length=100 , null=True , blank=True)
    country = models.CharField(max_length=100 , null=True , blank=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        verbose_name_plural = "StreamUsers"
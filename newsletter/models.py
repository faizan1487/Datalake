from django.db import models
# Create your models here.
class Newsletter(models.Model):
    first_name = models.CharField(max_length=100 , null=True , blank=True)
    phone = models.CharField(max_length=100 , null=True , blank=True)
    email = models.EmailField(unique=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    source = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"

    
    class Meta:
        verbose_name_plural = "Subscribers"
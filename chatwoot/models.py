from django.db import models
# Create your models here.
class ChatwoorUser(models.Model):
    first_name = models.CharField(max_length=100 , null=True , blank=True)
    phone = models.CharField(max_length=100 , null=True , blank=True)
    email = models.EmailField(unique=True, null=True , blank=True)
    city = models.CharField(max_length=100 , null=True , blank=True)
    country = models.CharField(max_length=100 , null=True , blank=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Chatwoot Users"
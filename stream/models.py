from django.db import models
# Create your models here.
class StreamUser(models.Model):
    first_name = models.CharField(max_length=100 , null=True , blank=True)
    last_name = models.CharField(max_length=100 , null=True , blank=True)
    email = models.EmailField(unique=True , null=True , blank=True)
    username = models.CharField(max_length=100 , null=True , blank=True)
    phone = models.CharField(max_length=100 , null=True , blank=True)
    country = models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "StreamUsers"
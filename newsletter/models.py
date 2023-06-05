from django.db import models
# Create your models here.
class Newsletter(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Subscribers"
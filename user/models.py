from django.db import models

# Create your models here.

#For MainSite (Al-Nafi) User:
class AlNafi_User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    address = models.CharField(max_length=25, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    verification_code = models.CharField(max_length=30, null=True, blank=True)
    isAffiliate = models.BooleanField(default=False)
    how_did_you_hear_about_us = models.CharField(max_length=255, null=True, blank=True)
    affiliate_code = models.CharField(max_length=255, null=True, blank=True)
    isMentor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.username
    
    class Meta:
        managed = True
        verbose_name = "Al-Nafi User"



#For Islamic Academy User/Customer:
class IslamicAcademy_User(models.Model):
    id = models.IntegerField(primary_key=True)
    is_paying_customer = models.BooleanField(default=False)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
    
    class Meta:
        managed = True
        verbose_name = "Islamic Academy User"
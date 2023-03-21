from django.db import models

# Create your models here.

#For MainSite User:
class AlnafiUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=25, null=True)
    address = models.TextField(null=True)
    country = models.CharField(max_length=255)
    language = models.CharField(max_length=255, null=True)
    verification_code = models.CharField(max_length=30)
    isAffiliate = models.BooleanField(default=False)
    how_did_you_hear_about_us = models.CharField(max_length=255, null=True)
    affiliate_code = models.CharField(max_length=255, null=True)
    isMentor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        managed = True
        verbose_name = "Al-Nafi User"



#For Islamic Academy User/Customer:
class IslamicAcademyUser(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    is_paying_customer = models.BooleanField()
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    role = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
    class Meta:
        managed = True
        verbose_name = "Islamic Academy User"
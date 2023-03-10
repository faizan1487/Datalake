from django.db import models

# Create your models here.

#For MainSite User:
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=50, default="PK")
    created_at= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.username
    class Meta:
        managed = True
        verbose_name = "Al-Nafi User"



#For Islamic Academy User/Customer:
class IslamicAcademyUser(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    is_paying_customer = models.BooleanField(default=False)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    role = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    class Meta:
        managed = True
        verbose_name = "Islamic Academy User"
